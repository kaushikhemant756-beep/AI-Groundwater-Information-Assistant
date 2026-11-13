from modules.groundwater_qa import answer_from_pdf

question = "What is groundwater recharge?"

print("\nUser Question:")
print(question)

print("\nAI Answer:")
answer = answer_from_pdf(question)
print(answer)
