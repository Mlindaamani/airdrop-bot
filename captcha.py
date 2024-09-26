from multicolorcaptcha import CaptchaGenerator

generator = CaptchaGenerator(captcha_size_num=5)


def generate_math_captcha() -> str:
    math_model = generator.gen_math_captcha_image(
        difficult_level=2,
        multicolor=False,
        allow_multiplication=True,
        margin=False
    )
    math_image = math_model.image
    math_equation_results = math_model.equation_result
    math_image.save('captcha_maze/math.png')
    return math_equation_results


def generate_image_captcha() -> str:
    image_model = generator.gen_captcha_image(
        difficult_level=2,
        multicolor=False,
        margin=False)
    image = image_model.image
    image_characters = image_model.characters
    image.save('captcha_maze/image.png')
    return image_characters


def main():
    ...


if __name__ == '__main__':
    main()
