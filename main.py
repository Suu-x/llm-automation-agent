import os
from dotenv import load_dotenv
from app import app

def main():

    load_dotenv(dotenv_path="../.env")
    print("Hello world!")
    app.run(debug=True)



if __name__ == "__main__":
    main()