import styles from "./Search.module.css"

const Search = () => {
	return (
		<div class={styles.search}>
			<input
				type="search"
				placeholder={`If it exist, there is a meme of it - search all the memes!`}
			/>
		</div>
	)
}
export default Search
