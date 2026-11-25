import sys
import tempfile
import types
from pathlib import Path
from PIL import Image

import image_storage as closet


def main():
    # Mock background removal
    sys.modules["rembg"] = types.SimpleNamespace(remove=lambda img: img)

    # Use a temporary database
    with tempfile.TemporaryDirectory() as tmp_dir:
        closet.DB_PATH = Path(tmp_dir) / "test_closet.db"

        # Save a sample image
        sample_img = Image.new("RGB", (64, 64), color=(0, 128, 255))

        item_id = closet.save_image(
            sample_img,
            name="Blue Shirt",
            category="Tops",
            colour="Blue",
            remove_background=True,
        )

        print(f"Saved item with id={item_id}")

        # Verify stored image
        saved_item = closet.get_image(item_id)

        assert saved_item is not None
        assert saved_item["name"] == "Blue Shirt"
        assert saved_item["category"] == "Tops"
        assert saved_item["colour"] == "Blue"
        assert isinstance(saved_item["image"], Image.Image)
        assert saved_item["image"].size == (64, 64)

        print("Verified saved image data and metadata.")

        # Test category and colour filters
        assert len(closet.get_images(category="Tops")) == 1
        assert len(closet.get_images(colour="Blue")) == 1
        assert len(closet.get_images(colour="Red")) == 0

        print("Image filters work correctly.")

        # Test deletion
        assert closet.delete_image(item_id) is True
        assert closet.get_image(item_id) is None

        print("Cleaned up test item successfully.")
        print("All tests passed!")


if __name__ == "__main__":
    main()
