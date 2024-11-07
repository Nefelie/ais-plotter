<script>
  import { onMount } from "svelte";
  import maplibregl from "maplibre-gl";

  let map;

  // Example data (replace this with your actual DataFrame or data)
  const points = [
    { longitude: -0.1278, latitude: 51.5074, name: "London" },
    { longitude: 2.3522, latitude: 48.8566, name: "Paris" },
    { longitude: 13.405, latitude: 52.52, name: "Berlin" },
  ];

  onMount(() => {
    // Initialize the Maplibre map
    map = new maplibregl.Map({
      container: "map", // The ID of the HTML container for the map
      style:
        "https://api.maptiler.com/maps/basic-v2/style.json?key=dFVEH9IaAa3jwgv9wt5D", // Maplibre tile URL
      center: [0, 0], // Map center in [longitude, latitude]
      zoom: 2, // Initial zoom level
    });

    // Add a GeoJSON source for the points
    const geoJsonData = {
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

    map.on("load", () => {
      map.addSource("points", {
        type: "geojson",
        data: geoJsonData,
      });

      // Add a layer to display the points
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
    });
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
