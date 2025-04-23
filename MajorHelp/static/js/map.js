document.addEventListener("DOMContentLoaded", function () {
    // Use Canvas rendering for better performance
    const map = L.map('map', { preferCanvas: true }).setView([37.8, -96], 4);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '© OpenStreetMap'
    }).addTo(map);

    // Use MarkerClusterGroup to group nearby markers for performance
    const markerCluster = L.markerClusterGroup({
        disableClusteringAtZoom: 8  // 👈 Tune this value
    });

    universities.forEach(u => {
        const icon = L.divIcon({
            className: "custom-marker",
            html: `<div style="background-color:${u.color}; width: 14px; height: 14px; border-radius: 50%; border: 2px solid white;"></div>`,
            iconSize: [16, 16],
            iconAnchor: [8, 8]
        });

        const marker = L.marker([u.lat, u.lng], { icon: icon })
            .bindTooltip(u.name, { direction: "top", opacity: 0.8 }) // Hover tooltips only
            .on("click", () => window.location.href = u.url);

        markerCluster.addLayer(marker);
    });

    map.addLayer(markerCluster);
});
