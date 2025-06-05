import os

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'jameskreye@gmail.com')


def send_confirmation_email(to_email, user_name, details):
    print("=== MOCK EMAIL ===")
    print(f"To: {to_email}")
    print(f"User: {user_name}")
    print("Details:")
    for k, v in details.items():
        print(f"  {k}: {v}")
    print("==================")