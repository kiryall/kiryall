from ultralytics import YOLO


def main():
    model = YOLO("yolo26n-obb.pt")
    model.train(data="data.yaml", epochs=40, imgsz=1024)


if __name__ == "__main__":
    main()
