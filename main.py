from dash import Dash, html

def main() -> None:
    app = Dash()
    app.title = "CaseStudy"
    app.layout = html.Div()
    app.run()

if __name__ == "__main__":
    main()