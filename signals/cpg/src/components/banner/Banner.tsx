import './Banner.scss'; 

type BannerItem = {
    id: number;
    icon: string;
    title: string;
    subtitle: string;
}; 

export const Banner = ({
    title, 
    subtitle, 
    rowItems,
}: {
    title:string;
    subtitle:string;
    rowItems: Array<BannerItem>;
}) => (
<div className="banner">
    <h1 className="banner_title">{title}</h1>
    <p className="banner_subtitle">{subtitle}</p>
    <hr />
    <div className="banner__row">
      {rowItems.map((x) => (
        <div className="banner__row__item" key={x.id}>
          <div className="banner__row__item__row">
            <span className={`Graffiti-icon ${x.icon} ap-font-32`} />
            <div className="banner__row__item__row__details">
              <p className="banner__row__item__row__details__title">
                {x.title}
              </p>
              <p className="banner__row__item__row__details__subtitle">
                {x.subtitle}
              </p>
            </div>
          </div>
       </div>
      ))}
    </div>
  </div>
);