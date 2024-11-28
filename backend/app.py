from app import create_app

app = create_app()

print("import_name:", app.import_name)
print("static_folder:", app.static_folder)
print("template_folder:", app.template_folder)

if __name__ == "__main__":
    app.run(debug=True,ssl_context='adhoc')
