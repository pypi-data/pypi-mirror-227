import outlines.models as models 
import outlines.text.generate as generate

model = models.transformers("gpt2-medium")
prompt = "Is Kohli the greatest batsman ever"
guided = generate.regex(model,r"\s*([Yy]es|[Nn]o|[Nn]ever|[Aa]lways)",max_tokens=30)(prompt)