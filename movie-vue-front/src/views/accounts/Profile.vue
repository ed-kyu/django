<template>
  <div>
      <br>
      <br>
    <div class="container d-flex justify-content-center my-5">
      <div v-if="profile" class="col-3">
        <img id="profile" :src="getProfileImage(profile.photo)" alt="">
        <p class="my-2 profile-font">{{ profile.username }}</p>
        <!-- <div class="dropper my-3 d-flex justify-content-center flex-column">
            <input type="file" @change="uploadImages" multiple accept="image/*">
            <span>Drag images here.</span>
        </div> -->
      </div>
      <div class="col-6">
          <div v-if="profile.username === this.$store.state.authUser.username">
              <h1>MY PROFILE</h1> <!--{{ profile.username }}-->
          </div>
          <div v-else>
              <h1>{{ profile.username }}</h1>
          </div>
        <h3 ># {{ profile.id }}</h3>
        "{{ profile.message }}"
      </div>
      <div class="col-3 d-flex align-items-center">
        <button class="btn-default btn-round" @click="followOrUnfollow">
        ❤️{{ hearts }}
        </button>
      </div>
    </div>
    <br>
    <br>
    <br>
    <!-- <button v-if="profile.id" @click="followOrUnfollow">팔로우</button> -->
    <!-- <button v-if="profile.username!=this.$store.state.authUser.username" @click="followOrUnfollow">팔로우</button> -->
    <div class="container my-2 d-flex justify-content-center">
        <h1 class="my-2 col-3">찜한 영화</h1>
    </div>
    <div class="my-5" v-if="lovings.length > 0">
        <!-- <carousel :autoplay="true" :nav="false" :dots="false" class="container"> class="container" -->
    <carousel :nav="false" :dots="false" :margin="10" :items="4" class="container top-carousel">
          <div v-for="(card) in lovings" :key="card.id" class="movieCard"> <!--mx-1 my-3 col-xs-4 col-sm-3 col-md-2-->
            <router-link :to="`movie/detail/${card.id}`">
                <img :src="getMovieImage(card)" alt="" class="card movieImage" data-info="">
            </router-link>
        </div> 
    </carousel>
    </div>
    <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
  </div>
</template>

<script>
import axios from 'axios'
import carousel from 'vue-owl-carousel'
import { mapActions } from 'vuex'

const SERVER_URL = process.env.VUE_APP_SERVER_URL
// getCoverFlow
export default {
    name: "Profile",
    components: {
        carousel,
    },
    data: function () {
        return {
            // username: this.$store.state.authUser.username, 
            username: this.$route.params.username,
            profile: null,
            hearts: null,
            followings: null,
            lovings: null,
        }
    },
    methods: {
        ...mapActions(['uploadImages']),
        getProfile: function() {
            axios({
                method: 'GET',
                url: `${SERVER_URL}/accounts/${this.username}`,
                headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`},
            })
            .then(res => {
                console.log(res.data)
                this.profile = res.data
                this.hearts = res.data.hearts_received
                this.followings = res.data.hearts_sending
            })
            .catch(err => {
                console.log(err)
            })
        },
        getMovieImage: function(card) {
            return "https://www.themoviedb.org/t/p/w200/" + card.poster_path
        },
        getProfileImage: function (path) {
          return `${SERVER_URL}${path}`
        },
        followOrUnfollow: function () {
            axios({
                method: 'POST',
                url: `${SERVER_URL}/accounts/${this.$route.query.username}/follow/`,
                headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`},
            })
            .then(res => {
                console.log(res.data)
                this.hearts = res.data.HeartsReceived
                this.followings = res.data.HeartsSending
            })
            .catch(err => {
                console.log(err)
            })
        },
        getLovings : function() {
            axios({
                method: 'GET',
                url: `${SERVER_URL}/accounts/${this.username}/favorites/`,
                headers: { Authorization: `JWT ${localStorage.getItem('jwt')}`},
            })
            .then(res => {
                console.log(res.data)
                this.lovings = res.data
            })
            .catch(err => {
                console.log(err)
            })
        },
        setProfilePath: function() {
          this.username = this.$route.query.username
            if (this.username===undefined){
                this.username = this.$store.state.authUser.username
            }
        },
        initProfilePath: function() {
            this.username = this.$store.state.authUser.username
        },
        
    },
    created: function() {
      this.setProfilePath()
      this.getProfile()
      this.getLovings()
      this.initProfilePath()
      console.log(this.username)
    },
}
</script>

<style scoped>
.btn-round {
    width: 85px;
    height: 85px;
    padding: 10px 16px;
    border-radius: 40px;
    font-size: 24px;
    line-height: 1.33;
}
.profile-font{
    font-size: 30px;
}
#profile {
  width: 150px;
  height: 150px;
  border-radius: 70%;
}

.movieCardSmall {
  display: inline-block;
  height: 200px;
  /* border-radius: 5px; */
  border-style: none;
  /* background-color: gray.100; */
  /* width: 200px; */
}
</style>