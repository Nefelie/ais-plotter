<script>
  import { onMount } from "svelte";
  import { Deck } from "@deck.gl/core";
  import { MaplibreLayer } from "@deck.gl/maplibre";
  import Maplibre from "maplibre-gl";
  import { ScatterplotLayer } from "@deck.gl/layers";

  let map;
  let deck;

  onMount(async () => {
    // Sample coordinates
    const coordinates = [
      [37.7749, -122.4194], // San Francisco
      [34.0522, -118.2437], // Los Angeles
      [40.7128, -74.006], // New York
    ];

    // Prepare the data for the ScatterplotLayer
    const data = coordinates.map((coord) => ({
      position: [coord[1], coord[0]], // [longitude, latitude]
      size: 10, // Marker size
    }));

    // Initialize Maplibre
    map = new Maplibre.Map({
      container: "map",
      style:
        "https://api.maptiler.com/maps/basic-v2/style.json?key=dFVEH9IaAa3jwgv9wt5D",
      center: [-95.7129, 37.0902], // Center of the US
      zoom: 3,
    });

    // Initialize Deck.gl
    deck = new Deck({
      initialViewState: {
        longitude: -95.7129,
        latitude: 37.0902,
        zoom: 3,
        pitch: 0,
        bearing: 0,
      },
      layers: [
        new MaplibreLayer({
          id: "maplibre-layer",
          map: map,
        }),
        new ScatterplotLayer({
          id: "scatterplot-layer",
          data,
          getPosition: (d) => d.position,
          getFillColor: [255, 0, 0],
          getRadius: 100,
          radiusMinPixels: 5,
          radiusMaxPixels: 30,
        }),
      ],
      controller: true,
    });
  });
</script>

<div id="map"></div>

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
