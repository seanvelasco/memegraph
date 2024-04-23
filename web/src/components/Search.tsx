import { createSignal, createEffect } from "solid-js"
import { useSearchParams, useNavigate } from "@solidjs/router"
import styles from "./Search.module.css"

const Search = (props: { count: number | undefined }) => {
	const navigate = useNavigate()
	const [searchParams, setSearchParams] = useSearchParams()
	const [search, setSearch] = createSignal(searchParams.query || "")

	createEffect(async () => {
		await navigate(search() ? "/search" : "/")
		setSearchParams({ query: search() })
	})

	const headline = "If it exists, there is a meme of it"

	const locale = (count: number) => Number(count).toLocaleString()

	const placeholder = () =>
		props.count
			? `${headline}... search among ${locale(props.count)} memes!`
			: headline

	return (
		<div class={styles.search}>
			<input
				type="search"
				value={search()}
				onInput={(event) => setSearch(event.target.value)}
				placeholder={placeholder()}
			/>
		</div>
	)
}

export default Search
