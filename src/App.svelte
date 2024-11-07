<script lang="ts">
  import { onMount } from "svelte";
  import maplibregl from "maplibre-gl"; // Import maplibregl for both types and runtime

  let map: maplibregl.Map; // Explicitly type the map as maplibregl.Map
  let points: { longitude: number; latitude: number; name: string }[] = []; // Declare points array

  // Function to fetch points data from the FastAPI backend
  async function fetchPoints() {
    const response = await fetch("http://127.0.0.1:8000/api/points"); // Fetch from backend
    if (response.ok) {
      const data = await response.json();
      console.log(data); // Add this line to debug
      points = data.points; // Store points data
      console.log("POINTS", points);
      updateMap(); // Update the map with the fetched points data
    } else {
      console.error("Failed to fetch points data");
    }
  }

  // Function to update the map with the fetched points
  function updateMap() {
    // Convert the points into GeoJSON format
    const geoJsonData: GeoJSON.FeatureCollection = {
      type: "FeatureCollection",
      features: points.map((point) => ({
        type: "Feature",
        geometry: {
          type: "Point",
          coordinates: [point.longitude, point.latitude],
        },
        properties: {
          name: point.name,
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
          "circle-radius": 6,
          "circle-color": "#FF5733",
          "circle-stroke-width": 2,
          "circle-stroke-color": "#ffffff",
        },
      });
    }
  }

  onMount(() => {
    if (maplibregl) {
      map = new maplibregl.Map({
        container: "map",
        style:
          "https://api.maptiler.com/maps/basic-v2/style.json?key=dFVEH9IaAa3jwgv9wt5D",
        center: [2.3522, 48.8566], // Paris coordinates
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
