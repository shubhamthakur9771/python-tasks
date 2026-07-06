from result_processor import ResultProcessor

processor = ResultProcessor()

processor.load_results()

processor.rank_students()

topper = processor.topper()

print("\n===== RESULT SUMMARY =====")

print()

print("Topper\n")

print(topper.name, "-", topper.total())

print()

print("Class Average :", round(processor.class_average(), 2))

print()

print("Pass Percentage :", round(processor.pass_percentage(), 2), "%")

processor.generate_report_cards()

print()

print("Report Cards Generated Successfully.")