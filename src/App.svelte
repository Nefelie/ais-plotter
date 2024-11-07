<script lang="ts">
  import { onMount } from "svelte";
  import maplibregl from "maplibre-gl";

  let map: maplibregl.Map;
  let points: { lat: number; lon: number; MMSI: number }[] = [];

  // Function to update the map with points data
  function updateMap() {
    console.log("Points array:", points);

    const geoJsonData: GeoJSON.FeatureCollection = {
      type: "FeatureCollection",
      features: points.map((point) => ({
        type: "Feature",
        geometry: {
          type: "Point",
          coordinates: [point.lon, point.lat],
        },
        properties: {
          MMSI: point.MMSI,
        },
      })),
    };

    if (map.getSource("points")) {
      (map.getSource("points") as maplibregl.GeoJSONSource).setData(
        geoJsonData
      );
    } else {
      map.addSource("points", {
        type: "geojson",
        data: geoJsonData,
      });

      map.addLayer({
        id: "points-layer",
        type: "circle",
        source: "points",
        paint: {
          "circle-radius": 1,
          "circle-color": "#000000",
        },
      });
    }
  }

  // Function to handle file upload and update map
  async function handleFileUpload(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input && input.files && input.files[0]) {
      const file = input.files[0];

      // Create a form data object to send the file to the server
      const formData = new FormData();
      formData.append("file", file);

      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/upload-pickle",
          {
            method: "POST",
            body: formData,
          }
        );

        if (response.ok) {
          const data = await response.json();
          if (data && Array.isArray(data.points)) {
            points = data.points;
            updateMap();
          } else {
            console.error("The 'points' field is missing or not an array.");
          }
        } else {
          console.error("Failed to upload and process pickle file");
        }
      } catch (error) {
        console.error("Error uploading file:", error);
      }
    }
  }

  onMount(() => {
    if (maplibregl) {
      map = new maplibregl.Map({
        container: "map",
        style:
          "https://api.maptiler.com/maps/basic-v2/style.json?key=dFVEH9IaAa3jwgv9wt5D",
        center: [2.3522, 48.8566],
        zoom: 5,
      });

      map.on("load", () => {
        console.log("Map loaded successfully!");
        fetchPoints();
      });
    }
  });
</script>

<div id="container">
  <div id="sidebar">
    <h1>AIS Data Plotter</h1>
    <label for="file-upload" class="button">Upload Pickle File</label>
    <input
      id="file-upload"
      type="file"
      accept=".pkl"
      on:change={handleFileUpload}
    />
  </div>
  <div id="map"></div>
</div>

<style>
  *,
  *::before,
  *::after {
    box-sizing: border-box;
  }
  html,
  body {
    margin: 0;
    padding: 0;
    height: 100%;
    width: 100%;
    overflow: hidden;
  }
  #container {
    display: flex;
    height: 100vh;
    width: 100vw;
  }
  #sidebar {
    width: 250px;
    padding: 20px;
    background-color: #f8f9fa;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
  #map {
    flex-grow: 1;
  }
  h1 {
    font-size: 1.5em;
    margin: 0 0 1em;
    color: #333;
  }
  .button {
    display: inline-block;
    padding: 8px 16px;
    margin-top: 10px;
    cursor: pointer;
    background-color: #007bff;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    text-align: center;
    text-decoration: none;
  }
  input[type="file"] {
    display: none;
  }
</style>
