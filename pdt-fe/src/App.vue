<template>
    <div id="app">
        <div class="container-fluid">
            <div class="row">
                <div class="col-2">
                    <div>
                        <b-button :pressed.sync="heatmap"
                                  variant="success" key="success">
                                Heatmapa
                        </b-button>
                    </div>
                    <div>
                        <b-card variant="primary">
                            Zvery v blizkosti
                            <b-collapse id="collapse1" class="mt-1"
                                        v-model="collapsed">
                                <b-form-group>
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

                    <div>
                        <b-form-select multiple :select-size="10"
                                       v-model="selectedAnimals" class="mb-3">
                            <option v-if="animals" v-for="animal in animals"
                                    :value="animal"> {{ animal }}
                            </option>
                        </b-form-select>
                    </div>

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

    export default {
        name: 'app',
        components: {
            Map
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
                heatmap: false,
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

            heatmap: function (val) {
                this.$refs.map.showHeatmap(val);
            },
        },

        methods: {
            fetchAnimals: function () {
                axios.get('http://127.0.0.1:5000/get_animals').then(response => {
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
        text-align: center;
        color: #2c3e50;
        margin-top: 60px;
    }

</style>
