from analyzer import ChatAnalyzer

chat = ChatAnalyzer()

chat.load_messages("chat_log.txt")

chat.write_errors("errors.log")

chat.sort_messages()

chat.export_chat("clean_chat_log.txt")

print("Top 5 Words Per Sender")
print("----------------------")

chat.top_five_words()

chat.longest_silence()