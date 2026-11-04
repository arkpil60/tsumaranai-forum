import argparse

from app.categories import create_category


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("title")
    parser.add_argument("--description", default="")

    args = parser.parse_args()

    category_id = create_category(
        slug=args.slug,
        title=args.title,
        description=args.description,
    )

    print(f"Created category #{category_id}")


if __name__ == "__main__":
    main()
