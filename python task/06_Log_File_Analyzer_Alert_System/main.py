from analyzer import LogAnalyzer

analyzer = LogAnalyzer()

analyzer.load_logs("app.log")

print("Level Frequency")

print(analyzer.level_frequency())

print()

analyzer.show_invalid()

print()

analyzer.write_errors("errors_only.log")

analyzer.error_alert()

print()

analyzer.most_common_error()