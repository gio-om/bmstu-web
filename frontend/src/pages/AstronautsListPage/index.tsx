import {Button, Col, Container, Form, Input, Row} from "reactstrap";
import {T_Astronaut} from "src/modules/types.ts";
import AstronautCard from "components/AstronautCard";
import {AstronautMocks} from "src/modules/mocks.ts";
import {FormEvent, useEffect} from "react";
import * as React from "react";

type Props = {
    astronauts: T_Astronaut[],
    setAstronauts: React.Dispatch<React.SetStateAction<T_Astronaut[]>>
    isMock: boolean,  
    setIsMock: React.Dispatch<React.SetStateAction<boolean>>
    astronautName: string,  // Параметр фильтрации
    setAstronautName: React.Dispatch<React.SetStateAction<string>>
}

// Через пропс получаем список астронавтов и параметр фильтрации
const AstronautsListPage = ({astronauts, setAstronauts, isMock, setIsMock, astronautName, setAstronautName}:Props) => {

    // Фильтруем после в хуке useEffect()
    const fetchData = async () => {
        try {
            const response = await fetch(`/api/astronauts/?astronaut_name=${astronautName.toLowerCase()}`)  // Фильтр на беке
            const data = await response.json()
            setAstronauts(data.astronauts)  // Обновляем значения стейта списка в App.tsx -> меняется пропс в AstronautListPage -> этот компонент перерендеривается 
            setIsMock(false)
        } catch {
            createMocks()  // Создаем через mock, если backend недоступен
        }
    }

    const createMocks = () => {      
        setIsMock(true)
        setAstronauts(AstronautMocks.filter(astronaut => astronaut.name.toLowerCase().includes(astronautName.toLowerCase())))  // Фильтр моков
    }

    const handleSubmit = async (e:FormEvent) => {  // При нажатии на кнопку вызов fetchData/создание моков
        e.preventDefault()
        if (isMock) {
            createMocks()
        } else {
            await fetchData()
        }
    }

    useEffect(() => {
        fetchData()
    }, []);

    return (
        <Container>
            <Row className="mb-5">
                <Col md="6">
                    <Form onSubmit={handleSubmit}>
                        <Row>
                            <Col md="8">
                                <Input value={astronautName} onChange={(e) => setAstronautName(e.target.value)} placeholder="Поиск..."></Input>
                            </Col>
                            <Col>
                                <Button color="primary" className="w-100 search-btn">Поиск</Button>
                            </Col>
                        </Row>
                    </Form>
                </Col>
            </Row>
            <Row>
                {astronauts?.map(astronaut => (
                    <Col key={astronaut.id} xs="4">
                        <AstronautCard astronaut={astronaut} isMock={isMock} />
                    </Col>
                ))}
            </Row>
        </Container>
    );
};

export default AstronautsListPage