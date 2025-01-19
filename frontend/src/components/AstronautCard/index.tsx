import {Button, Card, CardBody, CardImg, CardText, CardTitle} from "reactstrap";
import mockImage from "assets/mock.png";
import {Link} from "react-router-dom";
import {T_Astronaut} from "modules/types.ts";

interface AstronautCardProps {
    astronaut: T_Astronaut,
    isMock: boolean
}

const AstronautCard = ({astronaut, isMock}: AstronautCardProps) => {
    return (
        <Card key={astronaut.id} style={{width: '18rem', margin: "0 auto 50px", height: "calc(100% - 50px)" }}>
            <CardImg
                src={isMock ? mockImage as string : astronaut.image}
                style={{"height": "200px"}}
            />
            <CardBody className="d-flex flex-column justify-content-between">
                <CardTitle tag="h5">
                    {astronaut.name}
                </CardTitle>
                <CardText>
                    Время в космосе {astronaut.space_time}сут.
                </CardText>
                <Link to={`/astronauts/${astronaut.id}`}>
                    <Button color="primary">
                        Открыть
                    </Button>
                </Link>
            </CardBody>
        </Card>
    );
};

export default AstronautCard