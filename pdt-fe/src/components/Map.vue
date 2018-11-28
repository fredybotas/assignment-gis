<template>
    <div id="map">
        <l-map :zoom="zoom" :center="center" v-on:click="mapClick">
            <l-tile-layer :key="tileProvider.name" :name="tileProvider.name" :visible="tileProvider.visible" :url="tileProvider.url" :attribution="tileProvider.attribution"></l-tile-layer>
            <l-marker v-if="currMarker" :latLng="currMarker" v-on:click="removeMarker"></l-marker>
            <l-circle v-if="currMarker" :latLng="currMarker" :radius="radius * 1000" fillColor="red"></l-circle>
            <l-geo-json v-if="polygon" :geojson="polygon"></l-geo-json>
            <leaflet-heatmap v-if="heatmap" :lat-lng="heatmap" :max-zoom="11.5" :radius="100"></leaflet-heatmap>

        </l-map>
    </div>
</template>

<script>
    import Vue from 'vue';
    import { LCircle, LMap, LTileLayer, LMarker, LPolyline, LLayerGroup, LTooltip, LPopup, LControlZoom, LControlAttribution, LControlScale, LControlLayers, LGeoJson } from 'vue2-leaflet';
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
                gettingHeatmap: false,
                polygon: null,
                polygonIndex: null,
                heatmap: null,
                tileProvider: tileProvider,
                gradient: {0.4: 'blue', 0.65: 'lime', 1: 'red'},
                radius: 20,
            }
        },

        mounted: function () {

        },

        watch: {
          polygonIndex: function(val) {
              if(val === null) {
                    this.polygon = val;
                    return;
              }
              this.polygon = this.nearbyPolygons[val];
          }
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
            LCircle,
        },

        methods: {
            showPolygon: function(index) {
                if(index === null) {
                    this.polygon = index;
                    return;
                }

                this.polygon = this.nearbyPolygons[index];
            },

            showIntersectedPolygon: function(animals) {
                console.log(animals);
                if(animals.length === 0) {
                    return;
                }
                axios.get(process.env.VUE_APP_BACKEND+'get_animal', {params:
                    {
                        name:JSON.stringify(animals),
                    }
                }).then(response => {
                    console.log(response.data);
                    this.polygon = response.data;
                });
            },

            showHeatmap: function() {
                if(this.heatmap != null){
                    this.heatmap = null;
                    return;
                }
                if(this.gettingHeatmap === true){
                    return;
                }
                var arr = [];
                this.gettingHeatmap = true;
                this.$parent.heatmapButtonDisabled = true;
                axios.get(process.env.VUE_APP_BACKEND+'get_heatmap').then(response => {
                    response.data.map(point => {
                        var latlng = point['geometry']['coordinates'];
                        latlng = latlng.slice().reverse();
                        latlng.push(point['properties']['count']);
                        arr.push(latlng);
                    });
                    this.heatmap = arr;
                    this.gettingHeatmap = false;
                    this.$parent.heatmapButtonDisabled = false;
                });
            },



            mapClick: function (e) {
                this.currMarker = e['latlng'];
                this.polygon = null;
                this.$parent.animalsNearby = null;
                this.nearbyPolygons = null;
                axios.get(process.env.VUE_APP_BACKEND+'get_nearby', {params:
                    {
                        lat:e['latlng']['lat'],
                        lng:e['latlng']['lng'],
                        radius: this.radius * 1000
                    }
                }).then(response => {
                    this.nearbyPolygons = response.data;
                    this.$parent.showCollapse(response.data);
                });


            },

            refreshRadius: function (radius) {
                this.polygon = null;
                this.$parent.animalsNearby = null;
                this.nearbyPolygons = null;
                if(this.currMarker === null) {
                    return;
                }
                axios.get(process.env.VUE_APP_BACKEND+'get_nearby', {params:
                    {
                        lat:this.currMarker['lat'],
                        lng:this.currMarker['lng'],
                        radius: radius * 1000,
                    }
                }).then(response => {
                    this.nearbyPolygons = response.data;
                    this.$parent.showCollapse(response.data)
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
