import matplotlib.pyplot as plt


class RealtimeDrawing:
    def __init__(self, x_label=None, y_label=None, title=None, num_lines: int = 1, style=None):
        self.label = None
        names = self.__dict__
        for idx_line in range(num_lines):
            names["ax" + str(idx_line+1)] = []
            names["ay" + str(idx_line+1)] = []
        if style:
            plt.figure(figsize=(3.5, 2.5), dpi=200)
            plt.style.use(style)
        plt.ion()
        self.x_label = x_label
        self.y_label = y_label
        self.title = title
        self.num_lines = num_lines
        self.is_log_yscale = None
        self.is_log_xscale = None

    def add_data(self, x, y, label, idx_line=1):
        getattr(self, "ax" + str(idx_line)).append(x)
        getattr(self, "ay" + str(idx_line)).append(y)
        self.label = label

    def log_yscale(self):
        self.is_log_yscale = True

    def log_xscale(self):
        self.is_log_xscale = True

    def show(self):
        plt.show()

    def plot_data(self):
        plt.clf()
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        if self.is_log_yscale:
            plt.yscale("log")
        if self.is_log_xscale:
            plt.xscale("log")
        plt.title(self.title)
        for idx_line in range(self.num_lines):
            plt.plot(getattr(self, "ax" + str(idx_line+1)), getattr(self, "ay" + str(idx_line+1)), label=self.label)
        plt.legend()
        plt.pause(0.01)
        plt.ioff()


if __name__ == "__main__":
    dp = RealtimeDrawing("x", "y", "title", 2, style=["science", "ieee", "grid"])
    for i in range(50):
        dp.add_data(i, i ** 2, "label1", 1)
        dp.add_data(i, i, "label2", 2)
        dp.plot_data()
    show()
