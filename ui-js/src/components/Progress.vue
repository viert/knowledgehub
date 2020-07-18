<template>
  <div class="prg">
    <div class="prg-text">{{ text }}</div>
    <div class="prg-animation">
      <div class="prg-elem prg-elem--1"></div>
      <div class="prg-elem prg-elem--2"></div>
      <div class="prg-elem prg-elem--3"></div>
      <div class="prg-elem prg-elem--4"></div>
      <div class="prg-elem prg-elem--5"></div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      default: 'loading'
    }
  }
}
</script>

<style lang="scss">
.prg {
  width: 200px;
  margin: auto;
  text-align: center;
}

.prg-text {
  font-size: 2em;
  font-family: Montserrat;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.prg-animation {
  display: flex;
  justify-content: space-between;
  width: 100px;
  height: 20px;
  margin: auto;
}

.prg-elem {
  background-color: #cccccc;
  border: 1px solid #999999;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  animation: heartbeat 1s linear infinite;
}

.prg-elem--1 {
  animation-delay: 0.1s;
}
.prg-elem--2 {
  animation-delay: 0.2s;
}
.prg-elem--3 {
  animation-delay: 0.3s;
}
.prg-elem--4 {
  animation-delay: 0.4s;
}
.prg-elem--5 {
  animation-delay: 0.5s;
}

@keyframes heartbeat {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(2);
  }
  100% {
    transform: scale(1);
  }
}
</style>
