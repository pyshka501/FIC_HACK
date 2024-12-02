from g4f.client import Client

def convert_prompt(prompt: str, retry_times: int = 3) -> str:
    client = Client()

    text = prompt.strip()

    for i in range(retry_times):
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": 'Create an imaginative video descriptive caption or modify an earlier caption for the user input : "a girl is on the beach"',
                },
                {
                    "role": "assistant",
                    "content": "A radiant woman stands on a deserted beach, arms outstretched, wearing a beige trench coat, white blouse, light blue jeans, and chic boots, against a backdrop of soft sky and sea. Moments later, she is seen mid-twirl, arms exuberant, with the lighting suggesting dawn or dusk. Then, she runs along the beach, her attire complemented by an off-white scarf and black ankle boots, the tranquil sea behind her. Finally, she holds a paper airplane, her pose reflecting joy and freedom, with the ocean's gentle waves and the sky's soft pastel hues enhancing the serene ambiance.",
                },
                {
                    "role": "user",
                    "content": 'Create an imaginative video descriptive caption or modify an earlier caption for the user input : "A man jogging on a football field"',
                },
                {
                    "role": "assistant",
                    "content": "A determined man in athletic attire, including a blue long-sleeve shirt, black shorts, and blue socks, jogs around a snow-covered soccer field, showcasing his solitary exercise in a quiet, overcast setting. His long dreadlocks, focused expression, and the serene winter backdrop highlight his dedication to fitness. As he moves, his attire, consisting of a blue sports sweatshirt, black athletic pants, gloves, and sneakers, grips the snowy ground. He is seen running past a chain-link fence enclosing the playground area, with a basketball hoop and children's slide, suggesting a moment of solitary exercise amidst the empty field.",
                },
                {
                    "role": "user",
                    "content": 'Create an imaginative video descriptive caption or modify an earlier caption for the user input : " A woman is dancing, HD footage, close-up"',
                },
                {
                    "role": "assistant",
                    "content": "A young woman with her hair in an updo and wearing a teal hoodie stands against a light backdrop, initially looking over her shoulder with a contemplative expression. She then confidently makes a subtle dance move, suggesting rhythm and movement. Next, she appears poised and focused, looking directly at the camera. Her expression shifts to one of introspection as she gazes downward slightly. Finally, she dances with confidence, her left hand over her heart, symbolizing a poignant moment, all while dressed in the same teal hoodie against a plain, light-colored background.",
                },
                {
                    "role": "user",
                    "content": f'Create an imaginative video descriptive caption or modify an earlier caption in ENGLISH for the user input: "{text}"',
                },
            ],
            model="gpt-4o",
            temperature=0.01,
            top_p=0.7,
            stream=False,
            max_tokens=200,
        )
        if response.choices:
            return response.choices[0].message.content
    return prompt

if __name__ == "__main__":
    prompt = """Борис Петрович Иванов, 55-летний токарь завода "Металлист", посвятил свою жизнь нелегкому труду. После окончания профессионального училища он сразу устроился на завод и с тех пор проработал там более трех десятилетий.
    
    Опытный и умелый специалист, Борис прославился своими точными деталями и высоким качеством продукции. Он неустанно трудился, перевыполняя планы и обучая молодое поколение токарей. Его руки, испещренные шрамами и мозолями, свидетельствовали о его упорстве и преданности делу.
    
    Завод был как вторая семья для Бориса. Он участвовал в общественных мероприятиях, был наставником для молодых рабочих и пользовался уважением как среди коллег, так и начальства. Несмотря на тяжелую физическую работу, Борис всегда находил время для своей страсти к рыбалке и чтению.
    
    С выходом на пенсию Борис не забыл о своем любимом заводе. Он часто навещал своих бывших коллег и делился своим опытом и мудростью. Его жизнь стала примером силы и преданности к своему труду, оставив неизгладимый след в истории завода "Металлист"."""
    print()
    with open('test.txt', 'a') as f:
        t = convert_prompt(prompt)
        f.write(t)
        print(t)
