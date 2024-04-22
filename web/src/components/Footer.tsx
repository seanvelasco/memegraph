import styles from "./Footer.module.css"

const Footer = () => (
	<footer class={styles.footer}>
		<p>
			Built using{" "}
			<a href="https://openai.com/research/clip" target="_blank">
				OpenAI CLIP
			</a>
			by{" "}
			<a href="https://seanvelasco.com" target="_blank">
				sean.app
			</a>{" "}
			for{" "}
			<a
				href="https://supabase.com/blog/supabase-oss-hackathon"
				target="_blank"
			>
				Supabase Hackathon
			</a>
		</p>
	</footer>
)

export default Footer
