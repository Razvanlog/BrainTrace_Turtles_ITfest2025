// chatbot.js

document.addEventListener("DOMContentLoaded", function() {
    const currentLocationBtn = document.getElementById('current-location-btn');
    const searchLocationBtn = document.getElementById('search-location-btn');
    const locationInput = document.getElementById('location-input');
    const sortSelect = document.getElementById('sort-select');
    const resultsContainer = document.getElementById('results-container');
  
    // Insert your actual Google API Key here (make sure it matches the one in your HTML script tag)
    const GOOGLE_API_KEY = "...";
  
    // Base URLs for Google APIs
    const GEOCODE_API_URL = "https://maps.googleapis.com/maps/api/geocode/json";
    const PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json";
  
    let map;
    let markers = [];
  
    // Store current lat/lng so we can re-search when sort changes
    let currentLat = null;
    let currentLng = null;
  
    // Initialize the Google Map
    function initMap(center) {
      map = new google.maps.Map(document.getElementById("map"), {
        center: center,
        zoom: 14
      });
    }
  
    // Clear existing markers
    function clearMarkers() {
      markers.forEach(marker => marker.setMap(null));
      markers = [];
    }
  
    // Add a marker for a place with an info window
    function addMarker(place) {
      const position = {
        lat: place.geometry.location.lat,
        lng: place.geometry.location.lng
      };
      const marker = new google.maps.Marker({
        position: position,
        map: map,
        title: place.name
      });
      markers.push(marker);
  
      // Build content for the info window
      let contentString = `
        <div>
          <h3>${place.name}</h3>
          <p><strong>Rating:</strong> ${place.rating || "N/A"}</p>
          <p><strong>Address:</strong> ${place.vicinity || "N/A"}</p>
      `;
      // Include a photo if available
      if (place.photos && place.photos.length > 0) {
        const photoRef = place.photos[0].photo_reference;
        contentString += `<img src="https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${photoRef}&key=${GOOGLE_API_KEY}" alt="${place.name} photo">`;
      }
      contentString += `</div>`;
  
      const infowindow = new google.maps.InfoWindow({
        content: contentString
      });
  
      marker.addListener("click", () => {
        infowindow.open(map, marker);
      });
    }
  
    // Helper to handle a new lat/lng (either from geolocation or manual search)
    function handleLocation(lat, lng) {
      currentLat = lat;
      currentLng = lng;
      const center = { lat, lng };
      initMap(center);
      searchClinics(lat, lng);
    }
  
    // Automatically try to get user location on page load
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        position => {
          handleLocation(position.coords.latitude, position.coords.longitude);
        },
        error => {
          console.error("Geolocation error:", error);
          // If geolocation fails, user can enter location manually.
        }
      );
    } else {
      alert("Geolocation is not supported by your browser. Please enter a location manually.");
    }
  
    // Manual location search
    searchLocationBtn.addEventListener('click', () => {
      const location = locationInput.value.trim();
      if (location !== "") {
        geocodeAddress(location)
          .then(({ lat, lng }) => {
            handleLocation(lat, lng);
          })
          .catch(err => {
            console.error(err);
            alert("Error fetching location data.");
          });
      } else {
        alert("Please enter a location.");
      }
    });
  
    // When user changes sort (distance vs. rating), re-search if we have coordinates
    sortSelect.addEventListener('change', () => {
      if (currentLat !== null && currentLng !== null) {
        searchClinics(currentLat, currentLng);
      }
    });
  
    // Geocode an address to get latitude and longitude
    function geocodeAddress(address) {
      const url = `${GEOCODE_API_URL}?address=${encodeURIComponent(address)}&key=${GOOGLE_API_KEY}`;
      return fetch(url)
        .then(res => res.json())
        .then(data => {
          if (data.status === "OK" && data.results.length > 0) {
            const { lat, lng } = data.results[0].geometry.location;
            return { lat, lng };
          } else {
            throw new Error("Geocode failed");
          }
        });
    }
  
    // Search for oncology clinics using the Places API
    function searchClinics(lat, lng) {
      clearMarkers(); // Remove any previous markers
      const sort_by = sortSelect.value; // "distance" or "rating"
  
      const urlParams = new URLSearchParams({
        key: GOOGLE_API_KEY,
        keyword: "oncology clinic",
        location: `${lat},${lng}`
      });
  
      if (sort_by === "distance") {
        // rankby=distance does not allow a radius parameter
        urlParams.set("rankby", "distance");
      } else {
        // For rating sort, use a larger radius (e.g., 50 km)
        urlParams.set("radius", "50000");
      }
  
      const url = `${PLACES_API_URL}?${urlParams.toString()}`;
  
      fetch(url)
        .then(res => res.json())
        .then(data => {
          if (data.status === "OK") {
            // Limit to the first 5 results
            const results = data.results.slice(0, 5);
            displayResults(results, lat, lng);
          } else {
            console.error("Places API Error:", data.status);
            alert(`Error: ${data.status}. Could not fetch clinics.`);
          }
        })
        .catch(err => {
          console.error(err);
          alert("Error fetching clinic data.");
        });
    }
  
    // Display the search results in the list and add markers on the map
    function displayResults(places, userLat, userLng) {
      resultsContainer.innerHTML = "";
      if (!places || places.length === 0) {
        resultsContainer.innerHTML = "<p>No clinics found.</p>";
        return;
      }
  
      places.forEach(place => {
        // Add a marker for each place on the map
        addMarker(place);
  
        // Create a list item for the results container
        const div = document.createElement("div");
        div.className = "result-item";
        const name = place.name || "Unknown";
        const rating = place.rating || "N/A";
        const address = place.vicinity || "No address available";
  
        let photoHTML = "";
        if (place.photos && place.photos.length > 0) {
          const photoRef = place.photos[0].photo_reference;
          photoHTML = `<img src="https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${photoRef}&key=${GOOGLE_API_KEY}" alt="${name} photo">`;
        }
  
        // Optionally, compute the distance from the user (using Haversine)
        let distanceInfo = "";
        if (place.geometry && place.geometry.location) {
          const placeLat = place.geometry.location.lat;
          const placeLng = place.geometry.location.lng;
          const distKm = computeDistanceKm(userLat, userLng, placeLat, placeLng).toFixed(2);
          distanceInfo = `<p><strong>Distance:</strong> ${distKm} km</p>`;
        }
  
        div.innerHTML = `
          <h3>${name}</h3>
          ${photoHTML}
          <p><strong>Rating:</strong> ${rating}</p>
          <p><strong>Address:</strong> ${address}</p>
          ${distanceInfo}
        `;
        resultsContainer.appendChild(div);
      });
    }
  
    // Compute distance using the Haversine formula (corrected version)
    function computeDistanceKm(lat1, lng1, lat2, lng2) {
      const R = 6371; // Earth's radius in km
      const dLat = toRad(lat2 - lat1);
      const dLng = toRad(lng2 - lng1);
      const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
        Math.sin(dLng / 2) * Math.sin(dLng / 2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      return R * c;
    }
  
    function toRad(value) {
      return (value * Math.PI) / 180;
    }
  });
  
