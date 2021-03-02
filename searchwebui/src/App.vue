<template>
	<div id="app">
		<el-backtop :bottom="100" :visibility-height="650">
			<div class="back_top">
				UP
			</div>
		</el-backtop>
		<router-view/>
	</div>
</template>

<style>
#app {
	height: 100%;
}

.back_top {
	height: 100%;
	width: 100%;
	background-color: #f2f5f6;
	box-shadow: 0 0 6px rgba(0, 0, 0, .12);
	text-align: center;
	line-height: 40px;
	color: #1989fa;
}
</style>
<script>
export default {
	name: 'App'
}
</script>
