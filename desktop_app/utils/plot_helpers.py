def draw_equipment_charts(canvas, summary):
    dist = summary.get("type_distribution", {})
    fig = canvas.figure

    fig.clear()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    # Bar
    ax1.bar(dist.keys(), dist.values())
    ax1.set_title("Equipment Type Distribution (Bar)")
    ax1.tick_params(axis='x', rotation=45)

    # Pie
    ax2.pie(dist.values(), labels=dist.keys(), autopct="%1.1f%%")
    ax2.set_title("Pie Chart")

    canvas.draw()
