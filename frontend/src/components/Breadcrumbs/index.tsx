import {Breadcrumb, BreadcrumbItem} from "reactstrap";
import {Link, useLocation} from "react-router-dom";
import {T_Astronaut} from "modules/types.ts";

interface Props {
    selectedAstronaut: T_Astronaut | null
}

const Breadcrumbs = ({ selectedAstronaut }: Props) => {

    const location = useLocation()

    return (
        <Breadcrumb className="fs-5">
			{location.pathname == "/" &&
				<BreadcrumbItem>
					<Link to="/">
						Главная
					</Link>
				</BreadcrumbItem>
			}
			{location.pathname.includes("/astronauts") &&
                <BreadcrumbItem active>
                    <Link to="/astronauts">
						Астронавты
                    </Link>
                </BreadcrumbItem>
			}
            {selectedAstronaut &&
                <BreadcrumbItem active>
                    <Link to={location.pathname}>
                        { selectedAstronaut.name }
                    </Link>
                </BreadcrumbItem>
            }
			<BreadcrumbItem />
        </Breadcrumb>
    );
};

export default Breadcrumbs