/* @refresh reload */
import { render } from "solid-js/web"
import { MetaProvider } from "@solidjs/meta"
import { Router, Route, RouteLoadFuncArgs } from "@solidjs/router"
import App from "./App"
import { HomePage, SearchPage, ImagePage, getHome, getImages } from "./App"

const root = document.getElementById("root")

const loadHome = () => void getHome()

const loadImages = async ({ params }: RouteLoadFuncArgs) =>
	void getImages(params.image)

render(
	() => (
		<MetaProvider>
			<Router root={App}>
				<Route path="/" component={HomePage} load={loadHome} />
				<Route path="/search" component={SearchPage} />
				<Route path="/:image" component={ImagePage} load={loadImages} />
			</Router>
		</MetaProvider>
	),
	root!
)
