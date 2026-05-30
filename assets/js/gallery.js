import justifiedLayout from "./justified-layout.js";
import * as params from "@params";

const gallery = document.getElementById("gallery");

if (gallery) {
  let containerWidth = 0;
  const items = gallery.querySelectorAll(".gallery-item");

  const aspectRatios = Array.from(items).map((item) => {
    const img = item.querySelector("img");
    img.style.width = "100%";
    img.style.height = "auto";
    return parseFloat(img.getAttribute("width")) / parseFloat(img.getAttribute("height"));
  });

  const spacing = Number.isInteger(params.boxSpacing) ? params.boxSpacing : 8;
  const rowHeight = params.targetRowHeight || 288;

  // The bundled justified-layout leaves the final (incomplete) row at its natural
  // width, so a lone trailing photo creates a large gap. Stretch the last row to
  // fill the container width (preserving aspect ratios). A height cap prevents a
  // single widow from ballooning; when capped, the row is centered instead.
  function fillLastRow(layout) {
    const boxes = layout.boxes;
    if (!boxes.length) return;
    const lastTop = boxes.reduce((m, b) => Math.max(m, b.top), 0);
    const idx = [];
    boxes.forEach((b, i) => {
      if (Math.abs(b.top - lastTop) < 0.5) idx.push(i);
    });
    const curWidth = idx.reduce((w, i) => w + boxes[i].width, 0) + (idx.length - 1) * spacing;
    if (curWidth >= containerWidth - 1) return; // already full

    const ars = idx.map((i) => aspectRatios[i]);
    const sumAr = ars.reduce((a, c) => a + c, 0);
    const available = containerWidth - (idx.length - 1) * spacing;
    const fillHeight = available / sumAr;
    const height = Math.min(fillHeight, rowHeight * 1.9); // cap a lone-widow banner
    const widths = ars.map((ar) => ar * height);
    const totalWidth = widths.reduce((a, c) => a + c, 0) + (idx.length - 1) * spacing;
    let left = Math.max(0, (containerWidth - totalWidth) / 2); // 0 when filling; centers when capped
    idx.forEach((i, k) => {
      boxes[i].height = height;
      boxes[i].width = widths[k];
      boxes[i].left = left;
      left += widths[k] + spacing;
    });
    layout.containerHeight = lastTop + height;
  }

  function updateGallery() {
    if (containerWidth === gallery.getBoundingClientRect().width) return;
    containerWidth = gallery.getBoundingClientRect().width;

    const layout = justifiedLayout(aspectRatios, {
      rowWidth: containerWidth,
      spacing,
      rowHeight,
      heightTolerance: Number.isInteger(params.targetRowHeightTolerance) ? params.targetRowHeightTolerance : 0.25,
    });

    fillLastRow(layout);

    items.forEach((item, i) => {
      const { width, height, top, left } = layout.boxes[i];
      item.style.position = "absolute";
      item.style.width = width + "px";
      item.style.height = height + "px";
      item.style.top = top + "px";
      item.style.left = left + "px";
      item.style.overflow = "hidden";
    });

    gallery.style.position = "relative";
    gallery.style.height = layout.containerHeight + "px";
    gallery.style.visibility = "";
  }

  window.addEventListener("resize", updateGallery);
  window.addEventListener("orientationchange", updateGallery);

  // Call twice to adjust for scrollbars appearing after first call
  updateGallery();
  updateGallery();
}
