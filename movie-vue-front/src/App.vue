<template>
  <div id="app" class="app-bg pt-5">
    <nav class="navbar bg-transparent fixed-top nav-set" >
      <div class="container-fluid">
        <a class="navbar-brand" href="" onClick="top.location='javascript:location.reload()'">
          <img src="@/assets/carrot.png" class="bg-transparent" width="50" alt="">
        </a>
        <!-- <router-link class="navbar-brand" :to="{ name: 'Home' }">
          <img src="@/assets/carrot.png" class="bg-dark" width="50" alt="">
        </router-link> -->
        <div class="navbar"  v-if="isLogin">
          <router-link class="nav-link" @click.native="logout" to="#">로그아웃</router-link> |
          <router-link class="nav-link" :to="{ name: 'Home' }">Home</router-link> |
          <router-link class="nav-link" :to="{ name: 'Profile', query: {username: this.$store.state.authUser.username} }">MyProfile</router-link> 
        </div>
        <div class="navbar"  v-else>
          <router-link class="nav-link" :to="{ name: 'Signup' }">Signup</router-link> |
          <router-link class="nav-link" :to="{ name: 'Login' }">Login</router-link> 
        </div>
      </div>
    </nav>
    <router-view @login="isLogin=true"/>
  </div>
</template>

<script>
export default {
  name: 'App',
  data: function () {
    return {
      isLogin: false,
    }
  },
  methods: {
    logout: function () {
      this.isLogin = false
      localStorage.removeItem('jwt')
      this.$router.push({ name: 'Login' })
    }
  },
  created: function () {
    document.body.classList.add('app-bg')
    const token = localStorage.getItem('jwt')
    // this.$store.dispatch('LoadMovieCards')
    if (token) {
      this.isLogin = true
    }
    else {
      this.$router.push({ name: 'Login' })
    }
  }
}
</script>

<style lang="scss">
@import 'bootstrap/scss/bootstrap';
#app {
  font-family: Nanum_Gothic, Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: rgb(18, 18, 18);
  background-repeat: no-repeat;
  background-position: top;
  text-align: center;
  color: #cc289e;
}
@font-face {
  font-family: "Nanum_Gothic";
  src: local("Nanum_Gothic"),
   url('~@/assets/fonts/Nanum_Gothic/NanumGothic-Regular.ttf') format("truetype");
}

#nav {
  padding: 30px;
}

.nav-link {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  font-weight: bold;
  color: #cedbe8;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #cc289e;
}

.nav {
  height: 500px;
}
.simple-linear {
  background: linear-gradient(blue, pink);
}
.app-bg {
  background-color: rgb(18, 18, 18);
}
</style>
