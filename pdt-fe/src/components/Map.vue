<template>
    <div id="map">
        <l-map :zoom="zoom" :center="center" v-on:click="mapClick">
            <l-tile-layer :key="tileProvider.name" :name="tileProvider.name" :visible="tileProvider.visible" :url="tileProvider.url" :attribution="tileProvider.attribution"></l-tile-layer>
            <l-marker v-if="currMarker" :latLng="currMarker" v-on:click="removeMarker"></l-marker>
            <l-geo-json v-if="polygon" :geojson="polygon"></l-geo-json>
            <LeafletHeatmap v-if="heatmap" :lat-lng="heatmap" :max-zoom="11" :radius="80"></LeafletHeatmap>

        </l-map>
    </div>
</template>

<script>
    import Vue from 'vue';
    import { LMap, LTileLayer, LMarker, LPolyline, LLayerGroup, LTooltip, LPopup, LControlZoom, LControlAttribution, LControlScale, LControlLayers, LGeoJson } from 'vue2-leaflet';
    import axios from 'axios'
    import LeafletHeatmap from 'vue2-leaflet-heatmap'

    const tileProvider =
          {
              name: 'OpenStreetMap',
              visible: true,
              maxZoom: 18,
              attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
              url: 'https://api.mapbox.com/styles/v1/fredybotas/cjovkcus15jcq2ro410msq8d1/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZnJlZHlib3RhcyIsImEiOiJjam9odGhneTAwMXhxM2t0NjFndzdocjl3In0.eyQB1wwJxQ4MHgqQ7U7W7A'
          };

    export default {
        name: 'Map',
        props: {
            msg: String
        },

        data: function() {
            return {
                zoom: 8,
                center: [48.898518, 19.624874],
                points: [],
                polygons: [],
                slovakia: null,
                marker: null,
                currMarker: null,
                polygon: null,
                heatmap: null,
                tileProvider: tileProvider,
                gradient: {0.4: 'blue', 0.65: 'lime', 1: 'red'},
            }
        },

        mounted: function () {

        },


        components: {
            LMap,
            LTileLayer,
            LMarker,
            LPolyline,
            LLayerGroup,
            LTooltip,
            LPopup,
            LControlZoom,
            LControlAttribution,
            LControlScale,
            LControlLayers,
            LGeoJson,
            LeafletHeatmap,
        },

        methods: {
            fetchSlovakia: function () {
                Vue.http.get('http://127.0.0.1:5000/get_slovakia').then(response => {
                    this.slovakia = response.data[0];
                    let vm = this;
                    console.log(this.slovakia['json_build_object']);
                    L.geoJSON(this.slovakia['json_build_object']).addTo(this.mymap);
                });
            },

            showPolygon: function(index) {
                if(index === null) {
                    this.polygon = index;
                    return;
                }

                this.polygon = this.nearbyPolygons[index];
            },

            showIntersectedPolygon: function(animals) {
                console.log(animals);
                axios.get('http://127.0.0.1:5000/get_animal', {params:
                    {
                        name:animals[0],
                    }
                }).then(response => {
                    this.polygon = response.data;
                });
            },

            showHeatmap: function(state) {
                if(state === false){
                    this.heatmap = null;
                    return;
                }
                var arr = [];
                axios.get('http://127.0.0.1:5000/get_heatmap').then(response => {
                    response.data.map(point => {
                        var latlng = point['geometry']['coordinates'];
                        latlng = latlng.slice().reverse();
                        latlng.push(point['properties']['count']);
                        arr.push(latlng);
                    });
                    this.heatmap = arr;
                    console.log(this.heatmap);
                });
            },



            mapClick: function (e) {
                this.currMarker = e['latlng'];
                this.polygon = null;
                axios.get('http://127.0.0.1:5000/get_nearby', {params:
                    {
                        lat:e['latlng']['lat'],
                        lng:e['latlng']['lng'],
                        radius: 20000
                    }
                }).then(response => {
                    this.nearbyPolygons = response.data;
                    this.$parent.showCollapse(response.data);
                });


            },

            removeMarker: function () {
                this.currMarker = null;
                this.$parent.hideCollapse();
                this.nearbyPolygons = null;
                this.polygon = null;
            },
        },

    }


</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    #map {
        height: 800px;
    }
</style>
