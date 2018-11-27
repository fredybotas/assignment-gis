<template>

    <div id="app">
        <nav class="navbar navbar-light bg-light mb-2">
            <span class="navbar-brand mb-0 h1">PDT projekt Michal Manak</span>
        </nav>
        <div class="container-fluid">

            <div class="row">
                <div class="col-2">
                    <div class="mb-2">
                        <b-button :disabled="heatmapButtonDisabled"
                                  v-on:click="heatmapClicked"
                                  variant="secondary" key="secondary"
                                  style="width: 100%">
                            Heatmapa


                        </b-button>
                    </div>
                    <div class="mb-2">
                        <b-card variant="primary" class="mb-2">
                            Zvery na celom uzemi



                            <b-form-select multiple :select-size="10"
                                           v-model="selectedAnimals"
                                           class=" mt-2">
                                <option v-if="animals"
                                        v-for="animal in animals"
                                        :value="animal"> {{ animal }}



                                </option>
                            </b-form-select>

                        </b-card>

                    </div>
                    <div>
                        <b-card variant="primary" class="mb-2">
                            Zvery v blizkosti


                            <b-collapse id="collapse1" class="mt-1"
                                        v-model="collapsed">
                                <b-form-group
                                        style="max-height: 150px; overflow-y: scroll;">
                                    <b-form-radio-group stacked
                                                        v-model="selectedNearby"
                                                        name="radiosStacked">
                                        <b-form-radio
                                                v-for="(animal, index) in animalsNearby"
                                                :value="index"
                                                @onClick="animalSelected">
                                            {{ animal.properties.name }}



                                        </b-form-radio>
                                    </b-form-radio-group>
                                </b-form-group>
                            </b-collapse>
                        </b-card>

                    </div>
                    <b-form-slider v-model="sliderValue" :min="0" :max="100"
                                   trigger-change-event></b-form-slider>

                </div>
                <div class="col-10">
                    <Map ref="map"></Map>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

    import Map from './components/Map.vue'
    import axios from 'axios'
    import 'bootstrap/dist/css/bootstrap.css'
    import 'bootstrap-vue/dist/bootstrap-vue.css'
    import {bFormSlider} from 'vue-bootstrap-slider';


    export default {
        name: 'app',
        components: {
            Map,
            bFormSlider
        },

        mounted: function () {
            this.$nextTick(function () {
                this.fetchAnimals()
            })
        },

        data: function () {
            return {
                animals: null,
                collapsed: false,
                animalsNearby: null,
                selectedNearby: null,
                selectedAnimals: [],
                heatmapButtonDisabled: false,
                sliderValue: 0,
            }
        },

        watch: {
            selectedNearby: function (val) {
                this.$refs.map.showPolygon(val);
            },

            selectedAnimals: function (val) {
                this.$refs.map.removeMarker();
                this.$refs.map.showIntersectedPolygon(val);
            },
        },

        methods: {

            heatmapClicked: function () {
                this.$refs.map.showHeatmap();
            },

            fetchAnimals: function () {
                axios.get(process.env.VUE_APP_BACKEND + 'get_animals').then(response => {
                    this.animals = response.data;
                });
            },

            showCollapse: function (animals) {
                this.animalsNearby = animals;
                this.selectedNearby = null;
                this.collapsed = true;
            },

            hideCollapse: function () {
                this.animalsNearby = null;
                this.collapsed = false;
            },

            animalSelected: function () {
                console.log("selected animal");
            }
        },
    }
</script>

<style>
    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        color: #2c3e50;
    }

    .card-body {
        -ms-flex: 1 1 auto;
        -webkit-box-flex: 1;
        flex: 1 1 auto;
        padding: 0.5rem;
    }

</style>
