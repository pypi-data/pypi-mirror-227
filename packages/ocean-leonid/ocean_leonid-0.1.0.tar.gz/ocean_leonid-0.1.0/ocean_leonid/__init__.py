from .src import viz


def show_viz():
    app = viz()
    app.run_server(debug=True, host="0.0.0.0", port=8050)
