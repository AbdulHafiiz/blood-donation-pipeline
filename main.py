from code.load_data import load_data
from code.send_messages import send_messages
from code.generate_plots import generate_plots

def main():
    load_data()
    generate_plots()
    send_messages()

if __name__ == "__main__":
    main()