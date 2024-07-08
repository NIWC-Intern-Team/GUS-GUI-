class OuterClass:
    def __init__(self, outer_value):
        self.outer_value = outer_value
        self.inner_instance = self.InnerClass(self)

    def show_outer_value(self):
        print(f"Outer Value: {self.outer_value}")

    class InnerClass:
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance

        def show_both_values(self):
            # Accessing outer class attribute
            print(f"Outer Value: {self.outer_instance.outer_value}")

            # Inner class can also have its own attributes
            self.inner_value = "Inner Value"
            print(f"Inner Value: {self.inner_value}")

# Create an instance of the outer class
outer_instance = OuterClass("Outer Class Value")

# Use methods of the inner class to access outer class attributes
outer_instance.inner_instance.show_both_values()
