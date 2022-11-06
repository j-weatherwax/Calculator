from GUI import GUI

#Run main loop
def main():
    # Initialize window
    calculator_gui = GUI()
    
    # run main loop
    calculator_gui.start()

# If calc.py is being run normally, run the main function
# If calc.py is a module that's being imported by some other file, don't run main()
if __name__ == "__main__":
    main()