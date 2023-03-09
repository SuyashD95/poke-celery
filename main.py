import tasks

if __name__ == "__main__":
    result = tasks.add.delay(5, 10)
    while not (readiness := result.ready()):
        print(f"Result: {readiness}")
    print(f"Is Result Ready: {readiness}")
    print(f"Result: {result.get()}")
