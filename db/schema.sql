-- Initial relational sketch. Final schema may change with the chosen stack.

create table if not exists entries (
  id text primary key,
  schema_version integer not null,
  created_at timestamptz not null,
  event_date date not null,
  event_time time null,
  title text not null,
  body text not null,
  summary text not null,
  type text not null,
  scopes jsonb not null default '[]',
  tags jsonb not null default '[]',
  people jsonb not null default '[]',
  places jsonb not null default '[]',
  projects jsonb not null default '[]',
  mood text null,
  importance integer not null check (importance between 1 and 5),
  follow_ups jsonb not null default '[]',
  source jsonb not null,
  raw_input text not null,
  cleanup_level text not null check (cleanup_level in ('none', 'light', 'medium', 'heavy')),
  content_hash text not null,
  processing_notes jsonb not null default '[]',
  imported_at timestamptz not null default now()
);

create index if not exists entries_content_hash_idx on entries (content_hash);
create index if not exists entries_event_date_idx on entries (event_date);
create index if not exists entries_type_idx on entries (type);
