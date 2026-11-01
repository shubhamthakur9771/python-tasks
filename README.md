# PySpark: Building Reliable Batch I/O Pipelines — A Complete Beginner's Guide

Run this locally, top to bottom, in a notebook or `.py` script. Every topic has a plain
explanation, several runnable examples, and edge cases. All examples write sample files
to a local `./data` folder first, so everything is self-contained and reproducible.

---

## 0. Setup

```bash
pip install pyspark==3.5.1
```

```python
from pyspark.sql import SparkSession, Row
from pyspark.sql import functions as F
from pyspark.sql.types import *
import os, shutil

spark = (
    SparkSession.builder
    .appName("batch-io-guide")
    .master("local[*]")
    .config("spark.sql.shuffle.partitions", "4")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

# Fresh working directory for all examples in this guide
BASE = os.path.abspath("./spark_io_demo")
if os.path.exists(BASE):
    shutil.rmtree(BASE)
os.makedirs(BASE)
print("Working directory:", BASE)
```

We'll generate small sample files as we go, so you can run every example without needing
any external data.

---

## 1. `DataFrameReader` — The Entry Point for All Reads

Every read starts from `spark.read`, which returns a `DataFrameReader`. You configure it
with `.format(...)`, `.option(...)` / `.options(...)`, `.schema(...)`, then call a
terminal method like `.load(path)` or a format-specific shortcut like `.csv(path)`.

### Example 1.1 — the two equivalent styles

```python
# Style A: generic format() + load()
df = spark.read.format("csv").option("header", "true").load("some_path.csv")

# Style B: format-specific shortcut method (more common, less typing)
df = spark.read.option("header", "true").csv("some_path.csv")
```

Both produce identical results — shortcuts (`.csv()`, `.json()`, `.parquet()`, `.text()`,
`.orc()`, `.jdbc()`) just pre-set the format for you.

### Example 1.2 — `DataFrameReader` is reusable/chainable, and lazy

```python
reader = spark.read.option("header", "true").option("inferSchema", "true")
# Nothing has actually read any file yet — reads (like all Spark ops) are lazy until
# an action (show, count, write, collect...) is triggered.
```

---

## 2. `DataFrameWriter` — The Entry Point for All Writes

Every write starts from `df.write`, which returns a `DataFrameWriter`, configured the
same way (`.format()`, `.option()`, `.mode()`, `.partitionBy()`) then finished with a
terminal call like `.save(path)` or a shortcut like `.parquet(path)`.

### Example 2.1 — the two equivalent styles

```python
df.write.format("parquet").mode("overwrite").save("out_path")
df.write.mode("overwrite").parquet("out_path")   # shortcut, same result
```

### Example 2.2 — writers are also lazy until `.save()`/shortcut is called

```python
writer = df.write.mode("overwrite").option("compression", "snappy")
# nothing written yet
writer.parquet(os.path.join(BASE, "example"))   # NOW it writes
```

---

## 3. CSV Read

### Example 3.1 — create a sample CSV file to work with

```python
csv_path = os.path.join(BASE, "employees.csv")
with open(csv_path, "w") as f:
    f.write(
        "emp_id,name,salary,hire_date\n"
        "1,Alice,85000,2021-03-15\n"
        "2,Bob,72000,2020-07-01\n"
        "3,Carol,,2022-11-30\n"          # missing salary
        "4,Dave,91000,not-a-date\n"      # bad date value
    )
```

### Example 3.2 — basic read with header

```python
df_csv = spark.read.option("header", "true").csv(csv_path)
df_csv.show()
df_csv.printSchema()   # WITHOUT inferSchema, every column is read as StringType
```

### Example 3.3 — `inferSchema` (Spark scans the data to guess types)

```python
df_csv2 = spark.read.option("header", "true").option("inferSchema", "true").csv(csv_path)
df_csv2.printSchema()
# emp_id: integer, salary: integer/double (nulls allowed), hire_date: string
# (Spark's CSV inferSchema does NOT auto-detect dates by default — stays a string)
```

**Cost note:** `inferSchema=true` makes Spark do an **extra full pass** over the data
just to guess types, before the real read. On large files this roughly doubles read
time/cost — fine for exploration, avoid in production pipelines (use explicit schema
instead, Section 6).

### Example 3.4 — common CSV options together

```python
df_csv3 = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .option("sep", ",")                 # delimiter, e.g. ";" or "\t" for TSV
    .option("quote", '"')
    .option("escape", '"')
    .option("nullValue", "")            # treat empty string as null
    .option("dateFormat", "yyyy-MM-dd")
    .option("multiLine", "false")       # true if fields contain embedded newlines
    .option("ignoreLeadingWhiteSpace", "true")
    .option("ignoreTrailingWhiteSpace", "true")
    .csv(csv_path)
)
df_csv3.show()
```

### Edge case: CSV with no header

```python
csv_noheader = os.path.join(BASE, "no_header.csv")
with open(csv_noheader, "w") as f:
    f.write("1,Alice\n2,Bob\n")

df_nh = spark.read.option("header", "false").csv(csv_noheader)
df_nh.show()
# columns auto-named _c0, _c1 — always rename immediately:
df_nh = df_nh.toDF("id", "name")
```

---

## 4. JSON Read

### Example 4.1 — create a sample JSON-lines file (Spark's default JSON format)

```python
json_path = os.path.join(BASE, "employees.json")
with open(json_path, "w") as f:
    f.write('{"emp_id": 1, "name": "Alice", "salary": 85000}\n')
    f.write('{"emp_id": 2, "name": "Bob", "salary": null}\n')
    f.write('{"emp_id": 3, "name": "Carol", "salary": 91000, "bonus": 5000}\n')  # extra field
```

**Important:** Spark's default JSON reader expects **one JSON object per line**
("JSON Lines" / NDJSON), **not** a single JSON array spanning the whole file.

### Example 4.2 — basic read

```python
df_json = spark.read.json(json_path)
df_json.show()
df_json.printSchema()
# Spark automatically unions the schema across all lines -> "bonus" appears as a
# column for ALL rows, null where absent (schema inference merges fields seen anywhere)
```

### Example 4.3 — reading a "pretty-printed" / multi-line JSON array

```python
json_array_path = os.path.join(BASE, "employees_array.json")
with open(json_array_path, "w") as f:
    f.write("""[
  {"emp_id": 1, "name": "Alice"},
  {"emp_id": 2, "name": "Bob"}
]""")

df_json_multi = spark.read.option("multiLine", "true").json(json_array_path)
df_json_multi.show()
# WITHOUT multiLine=true here, Spark would fail to parse each line as standalone JSON
# and route every record to _corrupt_record (see Section 8)
```

### Example 4.4 — nested JSON produces nested (struct) schemas automatically

```python
nested_json = os.path.join(BASE, "nested.json")
with open(nested_json, "w") as f:
    f.write('{"id": 1, "address": {"city": "NYC", "zip": "10001"}}\n')

df_nested = spark.read.json(nested_json)
df_nested.printSchema()
df_nested.select("id", "address.city", "address.zip").show()
```

---

## 5. Parquet Read

Parquet is Spark's preferred columnar format — schema is embedded in the file itself,
so no `inferSchema` guessing is needed, reads are faster, and it supports predicate/
column pruning natively.

### Example 5.1 — write then read a Parquet file (round-trip demo)

```python
sample_df = spark.createDataFrame(
    [(1, "Alice", 85000.0), (2, "Bob", 72000.0)],
    ["emp_id", "name", "salary"]
)
parquet_path = os.path.join(BASE, "employees.parquet")
sample_df.write.mode("overwrite").parquet(parquet_path)

df_parquet = spark.read.parquet(parquet_path)
df_parquet.show()
df_parquet.printSchema()   # types come straight from the file, no inference needed
```

### Example 5.2 — Parquet directories contain multiple part-files, that's normal

```python
os.listdir(parquet_path)
# ['part-00000-....snappy.parquet', 'part-00001-....snappy.parquet', '_SUCCESS', ...]
# Spark ALWAYS writes a directory of part-files (one per partition), never a single
# flat file, unless you explicitly .coalesce(1) first (see Section 15).
```

### Example 5.3 — reading multiple Parquet files/directories at once

```python
spark.read.parquet(parquet_path, parquet_path).count()  # reading same path twice, demo only
# more realistically: spark.read.parquet("path/part1", "path/part2")
# or with a wildcard:
spark.read.parquet(os.path.join(BASE, "employees.parquet", "*.parquet"))
```

### Edge case: schema merging across Parquet files with different columns

```python
spark.conf.set("spark.sql.parquet.mergeSchema", "true")
# needed if you're reading multiple parquet files/partitions written at different times
# with slightly different schemas (e.g., a new column added later). Off by default
# because it adds overhead — only enable when you actually need it.
```

---

## 6. Text Read

Reads any plain text file as a DataFrame with a single `value: string` column, one row
per line. Useful for logs or unstructured data you'll parse yourself.

### Example 6.1 — basic text read

```python
text_path = os.path.join(BASE, "log.txt")
with open(text_path, "w") as f:
    f.write("2024-01-01 INFO start\n2024-01-01 ERROR failure\n2024-01-02 INFO ok\n")

df_text = spark.read.text(text_path)
df_text.show(truncate=False)
df_text.printSchema()   # root |-- value: string (nullable = true)
```

### Example 6.2 — `wholetext` option: read entire file as ONE row

```python
df_whole = spark.read.option("wholetext", "true").text(text_path)
df_whole.count()   # 1 row containing the entire file content
```

### Example 6.3 — parsing text lines manually (common pattern)

```python
parsed = df_text.withColumn("level", F.split(F.col("value"), " ")[1])
parsed.show(truncate=False)
```

---

## 7. JDBC Basics (reading from / writing to relational databases)

JDBC reads/writes need a driver jar on the classpath. Below shows the API shape; you'll
need to add `--jars` / `spark.jars.packages` pointing to the right driver (e.g.
`postgresql-42.x.x.jar`, `mysql-connector-j-x.x.x.jar`) to actually connect.

### Example 7.1 — basic JDBC read

```python
# Example only — requires a real running database + driver jar to execute.
jdbc_df = (
    spark.read
    .format("jdbc")
    .option("url", "jdbc:postgresql://localhost:5432/mydb")
    .option("dbtable", "public.employees")
    .option("user", "myuser")
    .option("password", "mypassword")
    .option("driver", "org.postgresql.Driver")
    .load()
)
```

### Example 7.2 — running local Spark with the Postgres driver auto-downloaded

```bash
# pass the driver as a Maven coordinate — Spark fetches it automatically
pyspark --packages org.postgresql:postgresql:42.7.3
```

```python
spark2 = (
    SparkSession.builder
    .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3")
    .getOrCreate()
)
```

### Example 7.3 — pushing a query down instead of a whole table (reduces data pulled)

```python
jdbc_query_df = (
    spark.read.format("jdbc")
    .option("url", "jdbc:postgresql://localhost:5432/mydb")
    .option("query", "SELECT emp_id, name FROM employees WHERE salary > 50000")
    .option("user", "myuser").option("password", "mypassword")
    .option("driver", "org.postgresql.Driver")
    .load()
)
```

### Example 7.4 — parallel reads with partitioning (avoids single-connection bottleneck)

```python
jdbc_parallel_df = (
    spark.read.format("jdbc")
    .option("url", "jdbc:postgresql://localhost:5432/mydb")
    .option("dbtable", "employees")
    .option("user", "myuser").option("password", "mypassword")
    .option("driver", "org.postgresql.Driver")
    .option("partitionColumn", "emp_id")   # must be numeric/date column
    .option("lowerBound", "1")
    .option("upperBound", "100000")
    .option("numPartitions", "8")
    .load()
)
# Without partitionColumn/bounds, Spark reads via ONE connection = one task = no
# parallelism, and can be very slow for large tables.
```

### Example 7.5 — writing to JDBC

```python
jdbc_df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/mydb") \
    .option("dbtable", "public.employees_copy") \
    .option("user", "myuser").option("password", "mypassword") \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()
```

### Edge cases

- Forgetting `.option("driver", ...)` often still "works" if the jar is on the
  classpath and JDBC can auto-detect it from the URL, but it's best practice to always
  set it explicitly to avoid ambiguous-driver errors when multiple DB jars are present.
- Password should never be hardcoded in real pipelines — use a secrets manager or
  environment variable and inject at runtime.
- `numPartitions` too high can overwhelm the source database with connections — size it
  based on what the DB can handle, not just Spark's cluster size.

---

## 8. Options (general patterns you'll reuse across all formats)

### Example 8.1 — `.option()` (single) vs `.options()` (dict, several at once)

```python
spark.read.option("header", "true").option("inferSchema", "true").csv(csv_path)

# equivalent, often cleaner:
spark.read.options(header="true", inferSchema="true").csv(csv_path)

# or from a plain dict:
opts = {"header": "true", "inferSchema": "true", "nullValue": "NA"}
spark.read.options(**opts).csv(csv_path)
```

### Example 8.2 — options are always strings, even for booleans/numbers

```python
# WRONG (works by accident sometimes, but not guaranteed) - avoid Python bools/ints
spark.read.option("header", True).csv(csv_path)     # Spark coerces this, but...
spark.read.option("header", "true").csv(csv_path)    # ...this is the correct, safe form
```

---

## 9. Header

Already touched on above — consolidated here since it's its own listed topic.

### Example 9.1 — `header=true` uses the first line as column names AND excludes it from data

```python
spark.read.option("header", "true").csv(csv_path).show()
```

### Example 9.2 — `header=false` (default) treats the first line as DATA, names columns `_c0`, `_c1`...

```python
spark.read.option("header", "false").csv(csv_path).show()
# the literal string "emp_id,name,salary,hire_date" row now appears as a DATA row!
```

### Example 9.3 — header option is CSV/text-family only — irrelevant for JSON/Parquet

```python
# JSON and Parquet carry field names in the data/schema itself — there's no "header"
# concept, so `.option("header", ...)` has no effect (and is silently ignored) there.
```

---

## 10. `inferSchema`

### Example 10.1 — off (default for CSV): everything becomes `StringType`

```python
spark.read.option("header", "true").csv(csv_path).printSchema()
# ALL columns: string — even emp_id, even salary
```

### Example 10.2 — on: Spark samples the data to guess types

```python
spark.read.option("header", "true").option("inferSchema", "true").csv(csv_path).printSchema()
```

### Example 10.3 — inference can guess "wrong" for your intent

```python
mixed_csv = os.path.join(BASE, "mixed.csv")
with open(mixed_csv, "w") as f:
    f.write("code\n007\n042\n123\n")

spark.read.option("header", "true").option("inferSchema", "true").csv(mixed_csv).printSchema()
spark.read.option("header", "true").option("inferSchema", "true").csv(mixed_csv).show()
# "007" becomes integer 7 — leading zeros LOST. If "code" is really a zip/ID string,
# this silently corrupts your data. Always use an explicit schema for ID-like fields.
```

### Example 10.4 — JSON/Parquet infer schema differently

JSON always infers types from the data (no separate flag — it's implicit). Parquet
never needs inference — types are stored in the file's embedded schema/metadata.

---

## 11. Explicit Schema on Read

The production-grade alternative to `inferSchema` — faster (no extra data scan), and
guarantees consistent types.

### Example 11.1 — defining and applying an explicit schema for CSV

```python
schema = StructType([
    StructField("emp_id", IntegerType(), nullable=True),
    StructField("name", StringType(), nullable=True),
    StructField("salary", DoubleType(), nullable=True),
    StructField("hire_date", StringType(), nullable=True),   # keep as string, parse later
])

df_explicit = spark.read.option("header", "true").schema(schema).csv(csv_path)
df_explicit.printSchema()
df_explicit.show()
```

### Example 11.2 — explicit schema on JSON

```python
json_schema = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("salary", DoubleType()),
])
spark.read.schema(json_schema).json(json_path).show()
```

### Example 11.3 — DDL-string shorthand for schemas (quicker to write)

```python
ddl_schema = "emp_id INT, name STRING, salary DOUBLE, hire_date STRING"
spark.read.option("header", "true").schema(ddl_schema).csv(csv_path).show()
```

### Example 11.4 — what happens when data doesn't match the explicit schema

```python
# "not-a-date" in hire_date is fine since we typed it as STRING.
# But if we'd typed salary as IntegerType and a row had "abc", by default that
# becomes NULL silently (permissive mode) rather than raising an error — see Section 12.
bad_schema = "emp_id INT, name STRING, salary INT, hire_date STRING"
spark.read.option("header", "true").schema(bad_schema).csv(csv_path).show()
# Carol's blank salary -> null (fine), but any truly non-numeric salary -> null too,
# with NO error by default — this is why explicit validation still matters.
```

---

## 12. `mode` — Corrupt-Record Handling Basics (read-time)

Controls how Spark reacts to malformed records while **reading** CSV/JSON. Three modes:
`PERMISSIVE` (default), `DROPMALFORMED`, `FAILFAST`.

### Example 12.1 — set up a file with a genuinely malformed row

```python
bad_csv = os.path.join(BASE, "bad.csv")
with open(bad_csv, "w") as f:
    f.write(
        "emp_id,name,salary\n"
        "1,Alice,85000\n"
        "2,Bob,72000,EXTRA_FIELD\n"   # too many fields -> malformed under strict schema
        "3,Carol,91000\n"
    )

strict_schema = "emp_id INT, name STRING, salary INT"
```

### Example 12.2 — `PERMISSIVE` (default): keeps all rows, puts bad ones aside

```python
df_permissive = (
    spark.read
    .option("header", "true")
    .option("mode", "PERMISSIVE")
    .option("columnNameOfCorruptRecord", "_corrupt_record")
    .schema(strict_schema.replace("INT)", "INT)") + ", _corrupt_record STRING")
    .csv(bad_csv)
)
df_permissive.show(truncate=False)
# malformed rows get nulls in normal columns + the raw line in _corrupt_record
# NOTE: _corrupt_record column must be explicitly added to your schema to see it!
```

### Example 12.3 — `DROPMALFORMED`: silently discards bad rows

```python
df_drop = (
    spark.read
    .option("header", "true")
    .option("mode", "DROPMALFORMED")
    .schema(strict_schema)
    .csv(bad_csv)
)
df_drop.show()
# Bob's malformed row is just GONE — no trace, no warning. Log row counts before/after
# in production so this doesn't silently eat data unnoticed.
```

### Example 12.4 — `FAILFAST`: raises an exception immediately on any bad record

```python
try:
    spark.read.option("header", "true").option("mode", "FAILFAST") \
        .schema(strict_schema).csv(bad_csv).show()
except Exception as e:
    print("FAILFAST raised an error as expected:", type(e).__name__)
```

### Edge case: `mode` for CSV vs JSON behaves consistently, but JSON corrupt records include the whole malformed JSON text

```python
bad_json = os.path.join(BASE, "bad.json")
with open(bad_json, "w") as f:
    f.write('{"emp_id": 1, "name": "Alice"}\n')
    f.write('{this is not valid json}\n')

df_bad_json = spark.read.option("mode", "PERMISSIVE") \
    .option("columnNameOfCorruptRecord", "_corrupt_record") \
    .schema("emp_id INT, name STRING, _corrupt_record STRING") \
    .json(bad_json)
df_bad_json.show(truncate=False)
```

**Practical recommendation:** use `PERMISSIVE` + `_corrupt_record` in a data-quality
gate at pipeline entry, count/log corrupt rows, and either route them to a
"quarantine" table or fail the pipeline if the corrupt rate exceeds a threshold.

---

## 13. CSV Write

### Example 13.1 — basic write

```python
out_csv = os.path.join(BASE, "out_csv")
sample_df.write.mode("overwrite").option("header", "true").csv(out_csv)
os.listdir(out_csv)
# multiple part-*.csv files + _SUCCESS marker, not one single file (see Section 18)
```

### Example 13.2 — common write options

```python
sample_df.write.mode("overwrite") \
    .option("header", "true") \
    .option("sep", ",") \
    .option("quote", '"') \
    .option("nullValue", "") \
    .option("dateFormat", "yyyy-MM-dd") \
    .csv(out_csv)
```

### Example 13.3 — reading it back to confirm round-trip

```python
spark.read.option("header", "true").option("inferSchema", "true").csv(out_csv).show()
```

---

## 14. JSON Write

### Example 14.1 — basic write (produces JSON-lines files, matching the read format)

```python
out_json = os.path.join(BASE, "out_json")
sample_df.write.mode("overwrite").json(out_json)
os.listdir(out_json)
```

### Example 14.2 — inspect the actual line format written

```python
part_file = [f for f in os.listdir(out_json) if f.startswith("part-")][0]
with open(os.path.join(out_json, part_file)) as f:
    print(f.read())
# {"emp_id":1,"name":"Alice","salary":85000.0}
# {"emp_id":2,"name":"Bob","salary":72000.0}
```

---

## 15. Parquet Write

### Example 15.1 — basic write (Parquet is the recommended default for pipeline stages)

```python
out_parquet = os.path.join(BASE, "out_parquet")
sample_df.write.mode("overwrite").parquet(out_parquet)
```

### Example 15.2 — why Parquet over CSV/JSON for intermediate pipeline data

Parquet stores its own schema + types (no re-inference needed downstream), is
columnar (faster analytical reads, column pruning), and compresses well by default
— generally the right default choice unless you specifically need a
human-readable/interchange format like CSV/JSON for external consumers.

---

## 16. Append / Overwrite / Ignore / Error (write modes)

Controls what happens when the destination path **already has data**.

### Example 16.1 — `overwrite`: replaces existing data entirely

```python
path = os.path.join(BASE, "mode_demo")
sample_df.write.mode("overwrite").parquet(path)
spark.read.parquet(path).count()   # 2

sample_df.limit(1).write.mode("overwrite").parquet(path)
spark.read.parquet(path).count()   # 1 -- old data is GONE, fully replaced
```

### Example 16.2 — `append`: adds new data alongside existing

```python
sample_df.write.mode("append").parquet(path)
spark.read.parquet(path).count()   # grows -- previous rows PLUS new ones
# WARNING: append does NOT deduplicate. Re-running the same append twice
# doubles your data. Always guard batch jobs against accidental re-runs.
```

### Example 16.3 — `ignore`: silently does nothing if the path already has data

```python
before_count = spark.read.parquet(path).count()
sample_df.write.mode("ignore").parquet(path)   # path exists -> this write is a no-op
after_count = spark.read.parquet(path).count()
assert before_count == after_count   # unchanged, no error, no write happened
```

### Example 16.4 — `error` / `errorifexists` (the DEFAULT mode if you don't specify one!)

```python
empty_path = os.path.join(BASE, "fresh_path")
sample_df.write.parquet(empty_path)   # fine, path is new

try:
    sample_df.write.parquet(empty_path)   # no .mode() specified -> defaults to "error"
except Exception as e:
    print("Raised as expected:", type(e).__name__)
    # AnalysisException: path file:... already exists
```

**Beginner trap:** forgetting `.mode(...)` entirely means every re-run of your script
will crash on the second execution, because the default is `error`/`errorifexists`.
Always set an explicit mode in real pipelines.

### Edge case: mode strings are case-insensitive but must be one of the 4 valid values

```python
sample_df.write.mode("Overwrite").parquet(path)   # works, case-insensitive
# sample_df.write.mode("truncate").parquet(path)  # INVALID -> raises an error,
#                                                     "truncate" is not a write mode
```

---

## 17. `partitionBy`

Splits output into a directory-per-value layout (Hive-style partitioning), enabling
downstream engines to skip entire directories when filtering on the partition column
("partition pruning") instead of scanning every file.

### Example 17.1 — basic partitioned write

```python
sales2 = spark.createDataFrame(
    [(2024, 1, "A", 100.0), (2024, 2, "A", 150.0),
     (2024, 1, "B", 200.0), (2025, 1, "A", 300.0)],
    ["year", "month", "region", "revenue"]
)
part_path = os.path.join(BASE, "sales_partitioned")
sales2.write.mode("overwrite").partitionBy("year", "month").parquet(part_path)
```

### Example 17.2 — inspect the resulting directory layout

```python
for root, dirs, files in os.walk(part_path):
    for d in dirs:
        print(os.path.join(root, d))
# .../year=2024/month=1
# .../year=2024/month=2
# .../year=2025/month=1
# each leaf directory holds the part-files for that partition combo
```

### Example 17.3 — reading back automatically reconstructs partition columns

```python
df_part = spark.read.parquet(part_path)
df_part.printSchema()   # year and month ARE present as columns again, read from paths
df_part.filter("year = 2024 AND month = 1").show()
# this filter triggers PARTITION PRUNING -- only the matching directory is scanned
```

### Edge case: high-cardinality partition columns create too many small files

```python
# BAD PRACTICE: partitioning by something like emp_id (thousands of unique values)
# creates thousands of tiny directories/files -> slow metadata operations, wasted space.
# Rule of thumb: partition by LOW-cardinality columns you frequently filter on
# (year, month, region, status) — not by IDs, timestamps-to-the-second, or free text.
```

---

## 18. Compression Basics

### Example 18.1 — Parquet default compression is `snappy` (fast, moderate ratio)

```python
sample_df.write.mode("overwrite").parquet(os.path.join(BASE, "compressed_default"))
# files are automatically named *.snappy.parquet
```

### Example 18.2 — choosing a different compression codec

```python
for codec in ["snappy", "gzip", "none"]:
    p = os.path.join(BASE, f"compressed_{codec}")
    sample_df.write.mode("overwrite").option("compression", codec).parquet(p)
    files = [f for f in os.listdir(p) if f.startswith("part-")]
    print(codec, "->", files[0])
# gzip: smaller files, slower to write/read
# snappy: bigger than gzip, but much faster -- best general-purpose default
# none: no compression at all, largest files, fastest write
```

### Example 18.3 — compression for CSV/JSON text output

```python
sample_df.write.mode("overwrite").option("compression", "gzip").json(
    os.path.join(BASE, "json_gzip")
)
os.listdir(os.path.join(BASE, "json_gzip"))
# part files end in .json.gz
```

### Edge case: compressed CSV/JSON is NOT natively splittable for some codecs

Gzip-compressed text files can't be split across multiple tasks the way `.snappy`
Parquet or uncompressed text can — a single large `.gz` file gets processed by exactly
one task, which can bottleneck parallelism. Prefer Parquet (block-splittable) for large
intermediate data, and reserve gzip CSV/JSON mainly for smaller exports meant for
external consumption.

---

## 19. File Paths

### Example 19.1 — local filesystem paths (what we've used throughout this guide)

```python
sample_df.write.mode("overwrite").parquet("/tmp/my_local_output")          # absolute
sample_df.write.mode("overwrite").parquet("relative_output_folder")        # relative to cwd
sample_df.write.mode("overwrite").parquet("file:///tmp/my_local_output2")  # explicit local URI
```

### Example 19.2 — reading multiple files via glob patterns

```python
spark.read.option("header", "true").csv(os.path.join(BASE, "*.csv")).show()
# picks up ALL .csv files directly in BASE (employees.csv, no_header.csv w/ mismatched
# schema might cause issues -- glob-reading assumes SAME schema across matched files)
```

### Example 19.3 — reading a list of explicit paths at once

```python
spark.read.parquet(
    os.path.join(BASE, "compressed_snappy"),
    os.path.join(BASE, "compressed_gzip"),
)  # union of both directories' data in one DataFrame
```

### Example 19.4 — cloud storage paths (shape only — needs credentials/config to run)

```python
# S3
spark.read.parquet("s3a://my-bucket/path/to/data")
# ADLS / Azure
spark.read.parquet("abfss://container@account.dfs.core.windows.net/path")
# GCS
spark.read.parquet("gs://my-bucket/path/to/data")
# HDFS
spark.read.parquet("hdfs://namenode:8020/path/to/data")
# These require the matching cloud connector jars + credentials configured in
# spark.conf / environment before they'll work — same DataFrameReader API otherwise.
```

### Edge case: trailing slashes and directory vs file confusion

```python
# Spark read/write paths for CSV/JSON/Parquet are DIRECTORIES, not single files,
# even though you pass what looks like one path. Don't expect a literal
# "output.parquet" FILE to exist — expect an "output.parquet/" DIRECTORY containing
# part-files. To get a genuinely single output file, combine with coalesce(1):

sample_df.coalesce(1).write.mode("overwrite").option("header", "true").csv(
    os.path.join(BASE, "single_file_csv")
)
# still a directory with ONE part-*.csv file inside + _SUCCESS -- there is no way to
# force Spark to name it exactly "output.csv" directly; rename the part-file afterward
# with normal filesystem operations if you need an exact filename.
```

---

## 20. Putting It Together: A Small Reliable Batch Pipeline

```python
def read_source(path, schema_ddl):
    return (
        spark.read
        .option("header", "true")
        .option("mode", "PERMISSIVE")
        .option("columnNameOfCorruptRecord", "_corrupt_record")
        .schema(schema_ddl + ", _corrupt_record STRING")
        .csv(path)
    )

def quarantine_bad_rows(df):
    good = df.filter(F.col("_corrupt_record").isNull()).drop("_corrupt_record")
    bad = df.filter(F.col("_corrupt_record").isNotNull())
    n_bad = bad.count()
    if n_bad > 0:
        print(f"WARNING: {n_bad} corrupt rows quarantined")
        bad.write.mode("append").json(os.path.join(BASE, "quarantine"))
    return good

raw = read_source(csv_path, "emp_id INT, name STRING, salary DOUBLE, hire_date STRING")
clean = quarantine_bad_rows(raw)

(
    clean.write
    .mode("overwrite")
    .option("compression", "snappy")
    .partitionBy("hire_date")
    .parquet(os.path.join(BASE, "curated", "employees"))
)

print("Pipeline complete. Rows written:", clean.count())
```

---

## Quick Reference Cheat Sheet

| Task | Code |
|---|---|
| Read CSV with header + inferred types | `spark.read.option("header","true").option("inferSchema","true").csv(path)` |
| Read CSV with explicit schema (production) | `spark.read.option("header","true").schema(ddl_or_StructType).csv(path)` |
| Read JSON lines | `spark.read.json(path)` |
| Read a pretty JSON array file | `spark.read.option("multiLine","true").json(path)` |
| Read Parquet | `spark.read.parquet(path)` |
| Read plain text | `spark.read.text(path)` |
| Read from a database | `spark.read.format("jdbc").option("url",...).option("dbtable",...).load()` |
| Capture corrupt records | `.option("mode","PERMISSIVE").option("columnNameOfCorruptRecord","_corrupt_record")` + include that column in schema |
| Drop bad rows silently | `.option("mode","DROPMALFORMED")` |
| Fail immediately on bad rows | `.option("mode","FAILFAST")` |
| Write, replacing existing data | `df.write.mode("overwrite").parquet(path)` |
| Write, adding to existing data | `df.write.mode("append").parquet(path)` |
| Write, no-op if path exists | `df.write.mode("ignore").parquet(path)` |
| Write, error if path exists (default!) | `df.write.parquet(path)` or `.mode("error")` |
| Partition output by column(s) | `df.write.partitionBy("year","month").parquet(path)` |
| Set compression codec | `.option("compression", "snappy" \| "gzip" \| "none")` |
| Force a single output file | `df.coalesce(1).write...` |

---

Run the blocks in order — later examples reuse `sample_df`, `BASE`, and files created
earlier in the file.