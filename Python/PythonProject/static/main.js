 const uploadBtn = document.getElementById("uploadBtn");
    const fileInput = document.getElementById("fileInput");
    const result = document.getElementById("result");
    const previewImg = document.getElementById("previewImg");

    uploadBtn.addEventListener("click", async () => {
      const file = fileInput.files[0];
      if (!file) {
        result.textContent = "Please select an image first.";
        return;
      }

      // Show preview
      previewImg.src = URL.createObjectURL(file);

      const formData = new FormData();
      formData.append("file", file);

      try {
         const res = await fetch("/upload", { method: "POST", body: formData });
        const data = await res.json();

        if (data.error) {
          result.textContent = "Error: " + data.error;
        } else {
          result.textContent = `Dimensions: ${data.width} x ${data.height}`;
        }
      } catch (err) {
        result.textContent = "Upload failed: " + err.message;
      }
    });