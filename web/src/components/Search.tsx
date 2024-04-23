import styles from "./Search.module.css"

const Search = (props: { count: number | undefined }) => (
	<div class={styles.search}>
		<input
			type="search"
			placeholder={
				props.count
					? `If it exist, there is a meme of it`
					: `If it exist, there is a meme of it - search among ${props.count} memes!`
			}
		/>
	</div>
)
export default Search
