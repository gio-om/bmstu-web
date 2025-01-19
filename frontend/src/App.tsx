import {useState} from "react";
import Header from "components/Header";
import Breadcrumbs from "components/Breadcrumbs";
import AstronautPage from "pages/AstronautPage";
import AstronautsListPage from "pages/AstronautsListPage";
import {Route, Routes} from "react-router-dom";
import {T_Astronaut} from "src/modules/types.ts";
import {Container, Row} from "reactstrap";
import HomePage from "pages/HomePage";
import "./styles.css"

function App() {

    const [astronauts, setAstronauts] = useState<T_Astronaut[]>([])

    const [selectedAstronaut, setSelectedAstronaut] = useState<T_Astronaut | null>(null)

    const [isMock, setIsMock] = useState(false);

    const [astronautName, setAstronautName] = useState<string>("")

    return (
        <div>
            <Header/>
            <Container className="pt-4">
                <Row className="mb-3">
                    <Breadcrumbs selectedAstronaut={selectedAstronaut} />
                </Row>
                <Row>
                    <Routes>
						<Route path="/" element={<HomePage />} />
                        <Route path="/astronauts/" element={<AstronautsListPage astronauts={astronauts} setAstronauts={setAstronauts} isMock={isMock} setIsMock={setIsMock} astronautName={astronautName} setAstronautName={setAstronautName}/>} />
                        <Route path="/astronauts/:id" element={<AstronautPage selectedAstronaut={selectedAstronaut} setSelectedAstronaut={setSelectedAstronaut} isMock={isMock} setIsMock={setIsMock}/>} />
                    </Routes>
                </Row>
            </Container>
        </div>
    )
}

export default App
