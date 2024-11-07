<script lang="ts">
  import { onMount } from "svelte";
  import maplibregl from "maplibre-gl"; // Import maplibregl for both types and runtime

  let map: maplibregl.Map; // Explicitly type the map as maplibregl.Map
  let points: { lat: number; lon: number; MMSI: number }[] = [];

  // Function to fetch points data from the FastAPI backend
  async function fetchPoints() {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/points"); // Fetch from backend
      if (response.ok) {
        const data = await response.json();
        console.log(data); // Log the entire response to verify

        // Check if 'data' contains 'points' and it's an array
        if (data && Array.isArray(data.points)) {
          points = data.points; // Correctly assign the points array from the response
          updateMap(); // Update the map with the fetched points data
        } else {
          console.error("The 'points' field is missing or not an array.");
        }
      } else {
        console.error("Failed to fetch points data");
      }
    } catch (error) {
      console.error("Error fetching points:", error);
    }
  }

  // Function to update the map with the fetched points
  function updateMap() {
    console.log("Points array:", points); // Debug the points array

    // Convert the points into GeoJSON format
    const geoJsonData: GeoJSON.FeatureCollection = {
      type: "FeatureCollection",
      features: points.map((point) => ({
        type: "Feature",
        geometry: {
          type: "Point",
          coordinates: [point.lon, point.lat], // Adjusted to match the incoming data
        },
        properties: {
          MMSI: point.MMSI, // You can display MMSI or any other relevant property
        },
      })),
    };

    // Check if source already exists, if so, update the data instead of adding it
    if (map.getSource("points")) {
      (map.getSource("points") as maplibregl.GeoJSONSource).setData(
        geoJsonData
      );
    } else {
      // Add the points to the map as a new source
      map.addSource("points", {
        type: "geojson",
        data: geoJsonData,
      });

      // Add a layer to display the points as circles
      map.addLayer({
        id: "points-layer",
        type: "circle",
        source: "points",
        paint: {
          "circle-radius": 2,
          "circle-color": "#000000",
        },
      });
    }
  }

  onMount(() => {
    if (maplibregl) {
      map = new maplibregl.Map({
        container: "map",
        style:
          "https://api.maptiler.com/maps/basic-v2/style.json?key=dFVEH9IaAa3jwgv9wt5D", // Map style URL
        center: [2.3522, 48.8566], // Default center (Paris coordinates)
        zoom: 5, // Set zoom level
      });

      map.on("load", () => {
        console.log("Map loaded successfully!");
        fetchPoints(); // Call fetchPoints to load the points after the map is loaded
      });
    }
  });
</script>

<!-- HTML element where the map will be rendered -->
<div id="map"></div>

<!-- Styles for the map -->
<style>
  html,
  body {
    margin: 0;
    padding: 0;
    height: 100%;
    width: 100%;
  }

  #map {
    height: 100vh; /* Full height of the viewport */
    width: 100vw; /* Full width of the viewport */
  }
</style>
