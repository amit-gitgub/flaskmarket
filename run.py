from market import app


# Check if run.py file is executed directly and not imported from somewhere else
if __name__ == '__main__':
    app.run(debug=True, port=7000)