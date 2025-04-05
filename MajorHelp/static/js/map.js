document.addEventListener("DOMContentLoaded", function () {
    const map = L.map('map').setView([37.8, -96], 4); // Center of the US

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '© OpenStreetMap'
    }).addTo(map);

    const universities = [
        { name: "Gonzaga University", lat: 47.6664, lng: -117.4023, color: "#002144", url: "/UniversityOverview/gonzagauniversity/" },
        { name: "University of Texas - Austin", lat: 30.2849, lng: -97.7341, color: "#BF5700", url: "/UniversityOverview/universityoftexasaustin/" },
        { name: "University of Southern California", lat: 34.0224, lng: -118.2851, color: "#990000", url: "/UniversityOverview/universityofsoutherncalifornia/" },
        { name: "College of Charleston", lat: 32.7834, lng: -79.9371, color: "#800000", url: "/UniversityOverview/collegeofcharleston/" },
        { name: "Virginia Tech", lat: 37.2296, lng: -80.4139, color: "#861F41", url: "/UniversityOverview/virginiatech/" },
        { name: "University of Georgia", lat: 33.9496, lng: -83.3750, color: "#BA0C2F", url: "/UniversityOverview/universityofgeorgia/" },
        { name: "University of Florida", lat: 29.6516, lng: -82.3248, color: "#0021A5", url: "/UniversityOverview/universityofflorida/" },
        { name: "Auburn", lat: 32.6034, lng: -85.4808, color: "#0C2340", url: "/UniversityOverview/auburn/" },
        { name: "Ohio State", lat: 40.0076, lng: -83.0309, color: "#BB0000", url: "/UniversityOverview/ohiostate/" },
        { name: "Costal Carolina", lat: 33.7930, lng: -79.0129, color: "#008080", url: "/UniversityOverview/costalcarolina/" },
        { name: "New York University", lat: 40.7291, lng: -73.9965, color: "#57068C", url: "/UniversityOverview/newyorkuniversity/" },
        { name: "University of North Carolina", lat: 35.9049, lng: -79.0469, color: "#7BAFD4", url: "/UniversityOverview/universityofnorthcarolina/" },
        { name: "Vanderbilt", lat: 36.1447, lng: -86.8027, color: "#CFAE70", url: "/UniversityOverview/vanderbilt/" },
        { name: "Notre Dame", lat: 41.7030, lng: -86.2380, color: "#00205B", url: "/UniversityOverview/notredame/" },
        { name: "University of Pennsylvania", lat: 39.9522, lng: -75.1932, color: "#011F5B", url: "/UniversityOverview/universityofpennsylvania/" },
        { name: "Duke", lat: 36.0014, lng: -78.9382, color: "#0736A4", url: "/UniversityOverview/duke/" },
        { name: "Yale", lat: 41.3163, lng: -72.9223, color: "#0F4D92", url: "/UniversityOverview/yale/" },
        { name: "The Citadel", lat: 32.7970, lng: -79.9583, color: "#A0C3D2", url: "/UniversityOverview/thecitadel/" },
        { name: "Furman", lat: 34.9249, lng: -82.4405, color: "#582C83", url: "/UniversityOverview/furman/" },
        { name: "Stanford", lat: 37.4275, lng: -122.1697, color: "#8C1515", url: "/UniversityOverview/stanford/" },
        { name: "Harvard", lat: 42.3770, lng: -71.1167, color: "#A51C30", url: "/UniversityOverview/harvard/" },
        { name: "MIT", lat: 42.3601, lng: -71.0942, color: "#8A8B8C", url: "/UniversityOverview/mit/" },
        { name: "Princeton", lat: 40.3431, lng: -74.6551, color: "#E87722", url: "/UniversityOverview/princetonuniversity/" },
        { name: "Clemson", lat: 34.6834, lng: -82.8374, color: "#F66733", url: "/UniversityOverview/clemson/" },
        { name: "UofSC", lat: 33.9940, lng: -81.0301, color: "#73000A", url: "/UniversityOverview/universityofsouthcarolinacolumbia/" }
    ];

    universities.forEach(u => {
        const icon = L.divIcon({
            className: "custom-marker",
            html: `<div style="background-color:${u.color}; width: 14px; height: 14px; border-radius: 50%; border: 2px solid white;"></div>`,
            iconSize: [16, 16],
            iconAnchor: [8, 8]
        });

        const marker = L.marker([u.lat, u.lng], { icon: icon })
            .addTo(map)
            .bindTooltip(u.name, { permanent: false, direction: "top" })
            .on("click", () => window.location.href = u.url);
    });
});
