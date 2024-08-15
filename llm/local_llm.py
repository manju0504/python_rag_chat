# from typing import List
# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch
#
#
# class LocalLLM:
#     def __init__(self, model_path: str):
#         self.tokenizer = AutoTokenizer.from_pretrained(model_path)
#         self.model = AutoModelForCausalLM.from_pretrained(model_path)
#
#         if torch.cuda.is_available():
#             self.model = self.model.to('cuda')
#
#     async def generate(self, prompt: str, max_length: int = 100) -> str:
#         inputs = self.tokenizer(prompt, return_tensors="pt")
#         if torch.cuda.is_available():
#             inputs = inputs.to('cuda')
#
#         with torch.no_grad():
#             outputs = self.model.generate(**inputs, max_length=max_length)
#
#         response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
#         return response.replace(prompt, "").strip()
#
#     async def generate_stream(self, prompt: str, max_length: int = 100) -> List[str]:
#         inputs = self.tokenizer(prompt, return_tensors="pt")
#         if torch.cuda.is_available():
#             inputs = inputs.to('cuda')
#
#         generated_tokens = []
#         for _ in range(max_length):
#             with torch.no_grad():
#                 output = self.model(**inputs)
#
#             next_token_logits = output.logits[0, -1, :]
#             next_token = torch.argmax(next_token_logits, dim=-1)
#
#             generated_tokens.append(next_token.item())
#
#             inputs = self.tokenizer(self.tokenizer.decode(generated_tokens), return_tensors="pt")
#             if torch.cuda.is_available():
#                 inputs = inputs.to('cuda')
#
#             yield self.tokenizer.decode([next_token.item()], skip_special_tokens=True)
#
#         return