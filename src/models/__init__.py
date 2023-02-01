import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT

from dotenv import load_dotenv

load_dotenv()
IS_PROD = os.environ['IS_PROD'] == 'True'
DB_CONN_URI = os.environ['DB_CONN_URI']
EVENT_GUILD_ID = os.getenv('EVENT_GUILD_ID')

engine = create_engine(DB_CONN_URI,
                       pool_size=50,
                       max_overflow=10,
                       pool_recycle=3600,
                       pool_pre_ping=True,
                       pool_use_lifo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Make an UnsignedInt that is compat with both sqlite and MariaDB
UnsignedInt = Integer()
UnsignedInt = UnsignedInt.with_variant(BIGINT(unsigned=True), 'mysql')
UnsignedInt = UnsignedInt.with_variant(BIGINT(unsigned=True), 'mariadb')

#__all__ = ['Session', 'Registration', 'ConvoState', 'Participant',
#           'TeamRegistration', 'Team', 'TeamParticipant', 'init_db']


# Make Database
def init_db():
    import logging
    log = logging.getLogger(os.getenv('logging_str'))
    log.info(f"[init_db: Start] IsProd: {IS_PROD}")

    if not IS_PROD:
        log.info(f"[init_db: Drop]")
        Base.metadata.drop_all(engine)

    log.info(f"[init_db: Create] IsProd: {IS_PROD}")

    Base.metadata.create_all(engine)

    if not IS_PROD:
        log.info(f"[init_db: Add]")
        with Session() as session:
            create_test_data(session)

    log.info(f"[init_db: End]")

def create_test_data(session):
    session.add_all([
        Registration(full_name='Testudo Turtle',
                     email='umd@test.test',
                     institution='UMD',
                     guild_id=EVENT_GUILD_ID),
        Registration(full_name='Bill the Goat',
                     email='navy@test.test',
                     institution='NAVY',
                     guild_id=EVENT_GUILD_ID),
        Registration(full_name='Chip Truegrit',
                     email='umbc@test.test',
                     institution='UMBC',
                     guild_id=EVENT_GUILD_ID),
        Registration(full_name='Testora Raptora',
                     email='mc@test.test',
                     institution='MC',
                     guild_id=EVENT_GUILD_ID),
        Registration(full_name='Judgy McJudgypants',
                     email='judge@test.test',
                     institution='UMD',
                     guild_id=EVENT_GUILD_ID,
                     role='Judge'),
        Registration(full_name='Helper O\'Hara',
                     email='volunteer@test.test',
                     institution='UMD',
                     guild_id=EVENT_GUILD_ID,
                     role='Volunteer'),
        Registration(full_name='Molly Mentorson',
                     email='mentor@test.test',
                     institution='UMD',
                     guild_id=EVENT_GUILD_ID,
                     role='Mentor'),
    ])
    session.commit()


class Registration(Base):
    __tablename__ = 'registrations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(UnsignedInt, nullable=False)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    institution = Column(String(255), nullable=False)
    role = Column(String(255), default='Participant')

    def __repr__(self):
        return f"<Registration(id={self.id}, full_name={self.full_name}, email={self.email}, " \
               f"institution={self.institution}, guild_id={self.guild_id})>"

class ConvoState(Base):
    __tablename__ = 'convo_state'

    id = Column(Integer, primary_key=True, autoincrement=True)
    discord_id = Column(UnsignedInt, nullable=False)
    guild_id = Column(UnsignedInt, nullable=False)
    conversation = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    email = Column(String(255))

    def __repr__(self):
        return f"<ConvoStep(guild_id={self.guild_id}, discord_id={self.discord_id}, "\
                f"conversation={self.conversation}, state={self.state}, email={self.email})>"

class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    discord_id = Column(UnsignedInt, nullable=False)
    guild_id = Column(UnsignedInt, nullable=False)
    email = Column(String(255), nullable=False)
    institution = Column(String(255), nullable=False)
    role = Column(String(255), default='Participant')

    def __repr__(self):
        return f"<Participant(id={self.id}, discord_id={self.discord_id}, " \
               f"email={self.email}, institution={self.institution}, role={self.role})>"

class TeamRegistration(Base):
    __tablename__ = 'team_registrations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(UnsignedInt, nullable=False)
    email = Column(String(255), nullable=False)
    team_name = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<TeamRegistration(id={self.id}, guild_id={self.guild_id}, " \
               f"email={self.email}, team_name={self.team_name})>"

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, autoincrement=True)
    guild_id = Column(UnsignedInt, nullable=False)
    team_name = Column(String(255), nullable=False)
    team_role_id = Column(UnsignedInt, nullable=False)

    def __repr__(self):
        return f"<Team(team_id={self.id},team_name={self.team_name},team_role_id={self.team_role_id}"\
               f",guild_id={self.guild_id})>"

class TeamParticipant(Base):
    __tablename__ = 'team_participants'

    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    participant_id = Column(Integer, ForeignKey("participants.id"))
    guild_id = Column(UnsignedInt, nullable=False)

    def __repr__(self):
        return f"<TeamParticipant(id={self.id}, team_id={self.team_id}, " \
               f"participant_id={self.participant_id}, guild_id={self.guild_id})>"
