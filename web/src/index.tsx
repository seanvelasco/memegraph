/* @refresh reload */
import { render } from "solid-js/web"
import { MetaProvider } from "@solidjs/meta"
import { Router, Route, RouteLoadFuncArgs } from "@solidjs/router"
import App from "./App"
import { HomePage, SearchPage, ImagePage, getHome, getImages } from "./App"
import Fallback from "./components/Fallback"

const root = document.getElementById("root")

render(
	() => (
		<MetaProvider>
			<Router root={App}>
				<Route path="/" component={HomePage} load={() => getHome()} />
				<Route path="/search" component={SearchPage} />
				<Route
					path="/:image"
					component={ImagePage}
					load={({ params }: RouteLoadFuncArgs) =>
						getImages(params.image)
					}
				/>
				<Route path="*" component={Fallback} />
			</Router>
		</MetaProvider>
	),
	root!
)
