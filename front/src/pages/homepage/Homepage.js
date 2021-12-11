import styles from "./Homepage.module.scss"
import Header from "../../components/header/Header";
import Heading from "../../components/heading/Heading";
import {useEffect, useState} from "react";
import {getGenres} from "../../api/genres";
import {getMovies} from "../../api/movies";
import {getDirectors} from "../../api/directors";
import MovieCardSet from "../../components/movieCardSet/MovieCardSet";
import Tag from "../../components/tag/Tag";
import Loader from "../../components/loader/Loader";
import axios from "axios";

export const Homepage = () => {
    const [genres, setGenres] = useState({loading: true, content: []});
    const [movies, setMovies] = useState({loading: true, content: []});
    const [directors, setDirectors] = useState({loading: true, content: []})

    const fonts = [
        'Amatic',
        'Bangers',
        'Fredericka the Great',
        'Indie Flower',
        'Kirang Haerang',
        'Rye',
        'Corinthia',
        'Smooch',
        'Sassy Frass',
        'Monoton',
        'Bungee Inline'
    ]
    useEffect(() => {
        const letters = document.querySelectorAll('.letter')
        let count = 0;
        const rollIntro = () => {
            letters.forEach(letter => {
                let randomFontIndex = Math.floor(Math.random()*fonts.length);
                let randomFont = fonts[randomFontIndex];
                letter.style.fontFamily = randomFont;
            })
        }
        let introAnimation = setInterval(function () {
            rollIntro();
            if (count>15000){clearInterval(introAnimation);}
            count++;
        },850);
    }, []);
    // function getMovies() {
    //     axios({
    //         method: "GET",
    //         url: `http://127.0.0.1:5000/movies/`
    //     }).then(response => {
    //         console.log(response)
    //         // setMovies(response.data ?? [])
    //         setMovies({loading: false, content: response.data ?? []})
    //         // setNumPages(response.data.total_pages)
    //         // console.log(response.data.results)
    //     })
    // }

    useEffect(() => {
        (async () => {
            const {data} = await getGenres();
            setGenres({loading: false, content: data});
        })();
        // getMovies();

        (async () => {
            const {data} = await getMovies("status=new");
            setMovies({loading: false, content: data});
        })();

        (async () => {
            const {data} = await getDirectors();
            setDirectors({loading: false, content: data});
        })();
    }, []);

    return (
        <div className={styles.Homepage}>
            <Header
                title="World Movies"
                subtitle="international collection in one step"
            >

            </Header>
            <div className={styles.Homepage__movieSet}>
                <Heading label="Новинки"/>
                {movies.loading && <Loader/>}
                <MovieCardSet
                    movies={movies.content}
                    limit={10}
                />
            </div>

            <div className={styles.Homepage__tagSet}>
                <Heading label="Жанры"/>
                {genres.loading && <Loader/>}
                {genres.content.map(genre => (
                    <Tag
                        key={genre.id}
                        id={genre.id}
                        label={genre.name}
                        type="genre"
                    />
                ))}
            </div>

            <div className={styles.Homepage__tagSet}>
                <Heading label="Режиссёры"/>
                {directors.loading && <Loader/>}
                {directors.content.map(genre => (
                    <Tag
                        key={genre.id}
                        id={genre.id}
                        label={genre.name}
                        type="director"
                    />
                ))}
            </div>
        </div>
    )
}